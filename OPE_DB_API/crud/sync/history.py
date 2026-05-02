from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List

from OPE_DB_API.registry import HISTORY_TABLE_REGISTRY
from OPE_DB_API.models.session import SessionMetadata


def fetch_history_after(
    db: Session,
    domain: str,
    after_ts: datetime,
    limit: int = 5000,
) -> List:
    """
    Fetch committed history rows whose session ended after a given timestamp.
    """

    history_model = HISTORY_TABLE_REGISTRY[domain]

    return (
        db.query(history_model)
        .join(
            SessionMetadata,
            SessionMetadata.session_id == history_model.session_id,
        )
        .filter(
            SessionMetadata.domain == domain,
            SessionMetadata.active.is_(False),
            SessionMetadata.ended_at.isnot(None),
            SessionMetadata.ended_at > after_ts,
        )
        .order_by(
            SessionMetadata.ended_at.asc(),
            history_model.history_id.asc(),
        )
        .limit(limit)
        .all()
    )