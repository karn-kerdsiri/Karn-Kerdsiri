# test ของ T-02: ความเร็วการค้นหาช่วงเวลาว่าง เมื่อมีคำขอพร้อมกัน
# AC-BKG-05 (NFR-PERF-01): p95 ไม่เกิน 2 วินาที
from concurrent.futures import ThreadPoolExecutor
from datetime import date, time as clock_time, timedelta
from threading import Barrier
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base, Slot
from app.db.session import get_db
from app.main import app


def test_FR_BKG_01_lists_slots_through_30_days(client, make_slot):
    last_in_range = make_slot(days_from_today=30)
    outside_range = make_slot(days_from_today=31)

    response = client.get("/slots", params={"package_code": "BASIC"})

    assert response.status_code == 200
    slot_ids = {slot["slot_id"] for slot in response.json()}
    assert last_in_range.id in slot_ids
    assert outside_range.id not in slot_ids


def test_AC_BKG_05(client, tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'concurrent-slots.db'}",
        connect_args={"check_same_thread": False},
        pool_size=200,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, autoflush=False)
    with session_factory.begin() as db:
        slot_date = date.today() + timedelta(days=1)
        db.add_all(
            [
                Slot(
                    slot_date=slot_date,
                    start_time=clock_time(hour, 0),
                    package_code="BASIC",
                    capacity=5,
                    remaining=5,
                )
                for hour in range(8, 18)
            ]
        )

    previous_override = app.dependency_overrides.get(get_db)

    def override_get_db():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    barrier = Barrier(200)

    def request_slots(_):
        barrier.wait()
        started = time.perf_counter()
        response = client.get("/slots", params={"package_code": "BASIC"})
        return response.status_code, time.perf_counter() - started

    try:
        with ThreadPoolExecutor(max_workers=200) as executor:
            results = list(executor.map(request_slots, range(200)))
    finally:
        if previous_override is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = previous_override
        engine.dispose()

    assert all(status_code == 200 for status_code, _ in results)
    durations = [duration for _, duration in results]
    durations.sort()
    p95 = durations[int(len(durations) * 0.95) - 1]
    assert p95 <= 2.0
