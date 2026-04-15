from sqlalchemy.orm import Session
from OPE_DB_API.registry import LIVE_TABLE_REGISTRY


def get_live_row(
    db: Session,
    domain: str,
    data_id: int,
):
    """
    Fetch a live data row by data_id.
    """
    model = LIVE_TABLE_REGISTRY[domain]
    return db.get(model, data_id)