from fastapi import Depends
from sqlalchemy.orm import Session

from OPE_DB_API.db import get_db_session


def db_session(code: str) -> Session:
    """
    FastAPI dependency for DB session.
    """
    return Depends(lambda: next(get_db_session(code)))
