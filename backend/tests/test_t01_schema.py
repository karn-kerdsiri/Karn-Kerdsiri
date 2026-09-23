import sys
from pathlib import Path

from sqlalchemy import inspect

repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

from backend.app.db.models import AuditLog, Base, Booking, Slot
from backend.app.db.session import get_engine


def test_T01_schema_exists_and_hides_id_card_fields():
    # Supports T-01 and verifies CON-TECH-01 plus IF-HIS-01.
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    assert {"slots", "bookings", "audit_logs"}.issubset(tables)

    booking_columns = inspector.get_columns("bookings")
    booking_column_names = {item["name"] for item in booking_columns}
    assert "hn" in booking_column_names
    assert "national_id" not in booking_column_names

    slot_columns = {item["name"] for item in inspector.get_columns("slots")}
    assert {"slot_date", "start_time", "package_code", "capacity", "remaining"}.issubset(slot_columns)

    assert Slot.__tablename__ == "slots"
    assert Booking.__tablename__ == "bookings"
    assert AuditLog.__tablename__ == "audit_logs"
