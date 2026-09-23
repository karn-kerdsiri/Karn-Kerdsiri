from __future__ import annotations

import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from backend.app.db.models import Base


def get_engine() -> Engine:
    # Supports CON-TECH-01 and keeps a test fallback for local development.
    database_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    engine = create_engine(database_url, future=True)
    return engine


def init_db() -> None:
    # Supports CON-TECH-01 and the schema creation required by T-01.
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
