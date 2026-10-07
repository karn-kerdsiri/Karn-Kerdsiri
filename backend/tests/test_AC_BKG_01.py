# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from sqlalchemy import select

from app.db.models import Booking
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


def test_TC_BKG_01_1_booking_succeeds(client, db, make_slot):
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    response = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ
    assert response.status_code == 201
    booking = db.scalar(select(Booking).where(Booking.id == response.json()["booking_id"]))
    assert booking is not None

    # Then: แสดงหมายเลขคิว (รอ Q-02) จึงยังไม่ตรวจ

    # Then: ที่นั่งว่างของช่วงนั้นเป็น 0
    db.refresh(slot)
    assert slot.remaining == 0


def test_TC_BKG_01_2_slot_full(client, db, make_slot):
    # Given: ยืนยันตัวตนแล้ว; ช่วง 09.00 น. เหลือ 1 ที่และผู้ใช้อีกคนยืนยันก่อน;
    # วันเดียวกันและวันถัดไปมีช่วงว่างอย่างน้อย 3 ช่วง
    slot = make_slot(start="09:00", remaining=1)
    make_slot(start="08:30", remaining=1)
    make_slot(start="09:30", remaining=1)
    make_slot(start="09:00", remaining=1, days_from_today=2)
    first_booking = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)
    assert first_booking.status_code == 201

    # When: ยืนยันการจองช่วง 09.00 น.
    other_user = {"Authorization": "Bearer verified:0005678"}
    response = client.post("/bookings", json={"slot_id": slot.id}, headers=other_user)

    # Then: แจ้ง "ช่วงเวลาเต็ม"
    assert response.status_code == 409
    assert response.json()["detail"] == "ช่วงเวลาเต็ม"

    # Then: ไม่มีรายการจองซ้อนเกิดขึ้น
    bookings = db.scalars(select(Booking).where(Booking.slot_id == slot.id)).all()
    assert len(bookings) == 1


def test_TC_BKG_01_3_unauthenticated(client, db, make_slot):
    # Given: ยังไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    response = client.post("/bookings", json={"slot_id": slot.id})

    # Then: ไม่เข้าถึงข้อมูลผู้รับบริการก่อนมีผลยืนยันตัวตน (IF-IDP-01)
    assert response.status_code != 201
    assert db.scalars(select(Booking).where(Booking.slot_id == slot.id)).all() == []
    # Then: รูปแบบการปฏิเสธและสถานะ HTTP spec ไม่ได้บอก
