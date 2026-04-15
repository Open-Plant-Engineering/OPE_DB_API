from typing import Generator
from sqlalchemy.orm import sessionmaker, Session

from OPE_DB_API.db.engine import get_engine


# ---------------------------------------------------------
# Session factory cache (engine -> sessionmaker)
# ---------------------------------------------------------

_SESSION_FACTORIES = {}


def _get_session_factory(code: str) -> sessionmaker:
    """
    Return a sessionmaker bound to the project's engine.
    """
    if code in _SESSION_FACTORIES:
        return _SESSION_FACTORIES[code]

    engine = get_engine(code)
    factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        future=True,
    )

    _SESSION_FACTORIES[code] = factory
    return factory


def get_db_session(code: str) -> Generator[Session, None, None]:
    """
    FastAPI-compatible database session dependency.

    Yields a session and ensures it is closed afterward.
    """
    SessionLocal = _get_session_factory(code)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
