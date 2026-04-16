from sqlalchemy.orm import Session
from OPE_DB_API.registry import OVERLAY_TABLE_REGISTRY
from OPE_DB_API.crud.session import validate_session_active

def stage_create(
    db: Session,
    domain: str,
    payload: dict,
):
    """
    Stage a CREATE operation in the session overlay.
    """
    validate_session_active(db, session_id=payload["session_id"])

    overlay_model = OVERLAY_TABLE_REGISTRY[domain]
    row = overlay_model(**payload)
    db.add(row)
    return row