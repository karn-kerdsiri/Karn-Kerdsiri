from __future__ import annotations

from datetime import date, datetime, time

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Slot(Base):
    # Supports FR-BKG-01, FR-BKG-06, ASM-01, CON-TECH-01
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slot_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    package_code: Mapped[str] = mapped_column(String(32), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    remaining: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="slot")


class Booking(Base):
    # Supports FR-BKG-02, FR-BKG-04, IF-HIS-01, IF-IDP-01
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hn: Mapped[str] = mapped_column(String(32), nullable=False)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id"), nullable=False)
    booking_date: Mapped[date] = mapped_column(Date, nullable=False)
    queue_no: Mapped[str | None] = mapped_column(String(32), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="confirmed")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    slot: Mapped[Slot] = relationship(back_populates="bookings")


class AuditLog(Base):
    # Supports DOM-PDPA-01
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor_id: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    hn: Mapped[str] = mapped_column(String(32), nullable=False)
    accessed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
