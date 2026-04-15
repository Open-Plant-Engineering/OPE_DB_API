from sqlalchemy.orm import Session
from OPE_DB_API.registry import OVERLAY_TABLE_REGISTRY


def stage_delete(
    db: Session,
    domain: str,
    overlay_id: int,
):
    """
    Stage a DELETE operation.
    Deletion is represented as value = None.
    """
    overlay_model = OVERLAY_TABLE_REGISTRY[domain]
    row = db.get(overlay_model, overlay_id)

    if row is None:
        raise ValueError("Overlay row not found")

    row.value = None
    db.add(row)
    return row
