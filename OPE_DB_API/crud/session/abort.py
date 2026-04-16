from sqlalchemy.orm import Session

from OPE_DB_API.registry import OVERLAY_TABLE_REGISTRY
from OPE_DB_API.crud.session import validate_session_active, close_session

def abort_session(
    db: Session,
    *,
    session_id: int,
    domain: str,
):
    """
    Abort an active session.

    - Clears overlay
    - Does NOT touch live data
    - Does NOT write history
    - Closes session
    """

    validate_session_active(db, session_id=session_id)

    Overlay = OVERLAY_TABLE_REGISTRY[domain]

    db.query(Overlay).filter(
        Overlay.session_id == session_id
    ).delete()

    close_session(db, session_id=session_id)