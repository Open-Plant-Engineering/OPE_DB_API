"""
History API Router

Exposes history replay endpoints over HTTP.

Responsibilities:
- Parse incremental history batches
- Validate session and cursor input
- Delegate execution to ReplicaEngine

This router contains NO business logic.
"""

from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from ope_core.domain.history import HistoryBatch
from ope_core.domain.session import SessionState
from ope_core.domain.cursor import ReplicationCursor
from ope_core.replica.engine import ReplicaEngine


router = APIRouter(prefix="/history", tags=["history"])


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------

class HistoryChange(BaseModel):
    op: str
    table: str
    data: Dict[str, Any] | None = None
    where: Dict[str, Any] | None = None


class HistoryRequest(BaseModel):
    batch_id: str
    created_at: datetime
    changes: List[HistoryChange]
    session_id: str
    current_cursor_position: str


class HistoryResponse(BaseModel):
    cursor_position: str
    cursor_updated_at: datetime


# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------

def get_replica_engine(request: Request) -> ReplicaEngine:
    """
    Retrieve ReplicaEngine from application state.
    """
    return request.app.state.replica_engine


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@router.post("/apply", response_model=HistoryResponse)
def apply_history_endpoint(
    data: HistoryRequest,
    replica_engine: ReplicaEngine = Depends(get_replica_engine),
) -> HistoryResponse:
    """
    Apply an incremental history batch to the local replica.

    This endpoint:
    - constructs domain objects
    - delegates execution to ReplicaEngine
    - returns the updated replication cursor
    """

    history = HistoryBatch(
        batch_id=data.batch_id,
        created_at=data.created_at,
        changes=[change.dict() for change in data.changes],
    )

    session = SessionState(
        session_id=data.session_id,
        started_at=datetime.utcnow(),
        ended_at=None,
        active=True,
    )

    current_cursor = ReplicationCursor(
        position=data.current_cursor_position,
        updated_at=datetime.utcnow(),
    )

    new_cursor: ReplicationCursor = replica_engine.apply_history(
        history=history,
        session=session,
        current_cursor=current_cursor,
    )

    return HistoryResponse(
        cursor_position=new_cursor.position,
        cursor_updated_at=new_cursor.updated_at,
    )