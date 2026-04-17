from sqlalchemy import Sequence
from sqlalchemy.engine import Engine
from OPE_DB_API.db.base import Base


def init_database(engine: Engine):
    """
    Initialize database-level objects.
    This must be idempotent.
    """

    # ✅ Create shared history sequence
    Sequence("history_id_seq").create(
        bind=engine,
        checkfirst=True,
    )

    # ✅ Create tables
    Base.metadata.create_all(bind=engine)