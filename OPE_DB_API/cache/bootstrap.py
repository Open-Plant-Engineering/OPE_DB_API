from sqlalchemy.engine import Engine
from OPE_DB_API.db.base import Base

# Import all models that must exist locally
# This is IMPORTANT: importing registers them with SQLAlchemy

from OPE_DB_API.models import (
    DbDataBase,
    DbDataHistoryBase,
    SessionMetadata,
)

# Import domain models to register tables
from OPE_DB_API.domains import *  # noqa


def bootstrap_local_database(engine: Engine) -> None:
    """
    Ensure all required local database tables exist.

    This function:
    - Registers all ORM models
    - Creates tables if missing
    - Is safe to call multiple times
    """
    Base.metadata.create_all(bind=engine)