from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List

from OPE_DB_API.registry import HISTORY_TABLE_REGISTRY, LIVE_TABLE_REGISTRY
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
    live_model = LIVE_TABLE_REGISTRY[domain]

    rows = (
        db.query(
            history_model.data_id,
            history_model.operation_type,
            history_model.new_value,
            live_model.attribute_id,
            live_model.node_id,
            SessionMetadata.ended_at,
        )
        .outerjoin(
            live_model,
            live_model.data_id == history_model.data_id,
        )
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

    return [
        {
            "data_id": r.data_id,
            "node_id": r.node_id,
            "attribute_id": r.attribute_id,
            "operation_type": r.operation_type,
            "new_value": r.new_value,
            "committed_at": r.ended_at
        }
        for r in rows
    ]