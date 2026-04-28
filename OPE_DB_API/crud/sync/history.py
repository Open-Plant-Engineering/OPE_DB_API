from sqlalchemy.orm import Session
from typing import List

from OPE_DB_API.registry import HISTORY_TABLE_REGISTRY


def fetch_history_after(
    db: Session,
    domain: str,
    after_history_id: int | None,
    limit: int = 5000,
) -> List:
    """
    Fetch committed history records after a given history_id.

    Results are ordered ASC by history_id.
    """
    model = HISTORY_TABLE_REGISTRY[domain]

    query = db.query(model)

    if after_history_id is not None:
        query = query.filter(model.history_id > after_history_id)

    return (
        query
        .order_by(model.history_id.asc())
        .limit(limit)
        .all()
    )