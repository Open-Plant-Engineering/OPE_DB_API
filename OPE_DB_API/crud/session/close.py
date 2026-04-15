from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from OPE_DB_API.models import SessionMetadata


def close_session(
    db: Session,
    *,
    session_id: int,
):
    """
    Close (deactivate) a session.
    """

    session = db.get(SessionMetadata, session_id)

    if session is None:
        raise ValueError("Session not found")

    if not session.active:
        return session

    session.active = False
    session.ended_at = func.now()

    db.add(session)
    return session