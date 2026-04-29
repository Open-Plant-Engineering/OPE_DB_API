from sqlalchemy.orm import Session
from OPE_DB_API.models import SessionMetadata


def start_session(
    db: Session,
    *,
    session_id: int,
    username: str | None = None,
    hostname: str | None = None,
    domain: str | None = None,
):
    """
    Start a new session.

    Session ID must be externally generated.
    """

    session = SessionMetadata(
        session_id=session_id,
        username=username,
        hostname=hostname,
        active=True,
        domain=domain,
    )

    db.add(session)
    return session