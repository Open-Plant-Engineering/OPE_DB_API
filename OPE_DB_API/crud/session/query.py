from sqlalchemy.orm import Session
from sqlalchemy.exc import MultipleResultsFound

from OPE_DB_API.models import SessionMetadata
from OPE_DB_API.errors import SessionNotActiveError

def get_active_session(
    db: Session,
    *,
    username: str | None = None,
    hostname: str | None = None,
):
    """
    Return the active session for a user/host combination.

    Returns None if no active session exists.
    """

    query = (
        db.query(SessionMetadata)
        .filter(SessionMetadata.active.is_(True))
    )

    if username is not None:
        query = query.filter(SessionMetadata.username == username)

    if hostname is not None:
        query = query.filter(SessionMetadata.hostname == hostname)

    try:
        return query.one_or_none()
    except MultipleResultsFound as exc:
        raise RuntimeError(
            "Multiple active sessions found; data integrity issue"
        ) from exc



def list_sessions(
    db: Session,
    *,
    username: str | None = None,
    hostname: str | None = None,
    active_only: bool = False,
):
    """
    List sessions with optional filters.
    """

    query = db.query(SessionMetadata)

    if username is not None:
        query = query.filter(SessionMetadata.username == username)

    if hostname is not None:
        query = query.filter(SessionMetadata.hostname == hostname)

    if active_only:
        query = query.filter(SessionMetadata.active.is_(True))

    return (
        query
        .order_by(SessionMetadata.started_at.desc())
        .all()
    )


def validate_session_active(
    db: Session,
    *,
    session_id: int,
):
    """
    Validate that a session exists and is still active.
    """

    session = db.query(SessionMetadata).filter(
        SessionMetadata.session_id == session_id,
        SessionMetadata.active.is_(True)
    ).one_or_none()

    if not session:
        raise SessionNotActiveError(session_id)

    return session