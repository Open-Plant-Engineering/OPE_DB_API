from sqlalchemy.orm import Session
from OPE_DB_API.registry import OVERLAY_TABLE_REGISTRY
from OPE_DB_API.crud.session import validate_session_active

def push_work(
    db: Session,
    *,
    domain: str,
    session_id: int,
    payload,
):
    """
    Stage a single attribute change into session overlay (bucket behavior).
    One row per data_id per session.
    """

    validate_session_active(db, session_id=session_id)

    Overlay = OVERLAY_TABLE_REGISTRY[domain]

    # Ensure bucket semantics: remove existing staged change for same data_id
    if payload.data_id is not None:
        db.query(Overlay).filter(
            Overlay.data_id == payload.data_id
        ).delete()

    data_id = payload.data_id

    row = Overlay(
        data_id=data_id,
        session_id=session_id,
        node_id=payload.node_id,
        attribute_id=payload.attribute_id,
        operation_type=payload.operation_type,
        value=payload.value,
    )

    db.add(row)
    return row