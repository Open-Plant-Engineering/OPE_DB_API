from sqlalchemy.orm import Session
from OPE_DB_API.registry import HISTORY_TABLE_REGISTRY


def write_history(
    db: Session,
    domain: str,
    payload: dict,
):
    """
    Write a history record.
    Payload must already contain externally generated history_id.
    """
    history_model = HISTORY_TABLE_REGISTRY[domain]
    payload.pop("history_id", None)
    row = history_model(**payload)
    db.add(row)
    return row