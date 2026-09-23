from __future__ import annotations

from sqlalchemy.engine import Engine

from backend.app.db.models import Base


def upgrade(engine: Engine) -> None:
    # Supports CON-TECH-01, DOM-PDPA-01, IF-HIS-01.
    Base.metadata.create_all(bind=engine)


def downgrade(engine: Engine) -> None:
    # Supports rollback of the initial booking schema.
    Base.metadata.drop_all(bind=engine)
