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

    row = None
    if payload.data_id is not None:
        row = db.query(Overlay).filter(
            Overlay.data_id == payload.data_id,
            Overlay.session_id == session_id,
        ).one_or_none()

    # -------------------------
    # CREATE stays CREATE
    # -------------------------
    if row and row.operation_type == 1:
        if payload.operation_type == 3:
            row.operation_type = 3
            row.value = None
        else:
            row.value = payload.value
        return row

    # -------------------------
    # UPDATE or DELETE on UPDATE
    # -------------------------
    if row:
        if payload.operation_type == 3:
            row.operation_type = 3
            row.value = None
        else:
            row.operation_type = 2
            row.value = payload.value
        return row

    # -------------------------
    # New overlay entry
    # -------------------------
    row = Overlay(
        data_id=payload.data_id,
        session_id=session_id,
        node_id=payload.node_id,
        attribute_id=payload.attribute_id,
        operation_type=payload.operation_type,
        value=payload.value,
    )
    db.add(row)

    return row
