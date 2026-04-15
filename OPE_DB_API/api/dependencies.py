from typing import Generator
from sqlalchemy.orm import Session

from OPE_DB_API.db.session import get_db_session


def db_session(code: str) -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a SQLAlchemy Session
    for the given project code.
    """
    yield from get_db_session(code)
