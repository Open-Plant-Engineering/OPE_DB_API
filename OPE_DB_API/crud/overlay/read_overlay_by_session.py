from sqlalchemy.orm import Session
from OPE_DB_API.registry import OVERLAY_TABLE_REGISTRY


def read_overlay_by_session(
    db: Session,
    domain: str,
    session_id: int,
):
    overlay_model = OVERLAY_TABLE_REGISTRY[domain]

    return (
        db.query(overlay_model)
        .filter(overlay_model.session_id == session_id)
        .all()
    )