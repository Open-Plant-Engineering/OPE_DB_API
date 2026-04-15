from sqlalchemy.orm import Session
from OPE_DB_API.registry import OVERLAY_TABLE_REGISTRY


def stage_update(
    db: Session,
    domain: str,
    overlay_id: int,
    new_value,
):
    """
    Stage an UPDATE operation by replacing overlay value.
    """
    overlay_model = OVERLAY_TABLE_REGISTRY[domain]
    row = db.get(overlay_model, overlay_id)

    if row is None:
        raise ValueError("Overlay row not found")

    row.value = new_value
    db.add(row)
    return row
