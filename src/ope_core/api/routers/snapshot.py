"""
Snapshot API Router

Exposes snapshot application endpoints over HTTP.

This router is responsible for:
- Request parsing
- Input validation
- Delegating to ReplicaEngine

No business logic is implemented here.
"""

from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from ope_core.domain.snapshot import Snapshot
from ope_core.domain.session import SessionState
from ope_core.domain.cursor import ReplicationCursor
from ope_core.replica.engine import ReplicaEngine


router = APIRouter(prefix="/snapshot", tags=["snapshot"])


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------

class SnapshotRequest(BaseModel):
    snapshot_id: str
    created_at: datetime
    payload: Dict[str, Any]
    session_id: str


class SnapshotResponse(BaseModel):
    cursor_position: str | None
    cursor_updated_at: datetime | None


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

@router.post("/apply", response_model=SnapshotResponse)
def apply_snapshot_endpoint(
    data: SnapshotRequest,
    replica_engine: ReplicaEngine = Depends(get_replica_engine),
) -> SnapshotResponse:
    """
    Apply an authoritative snapshot to the local replica.

    This endpoint:
    - creates domain objects
    - calls ReplicaEngine
    - returns the new replication cursor
    """

    snapshot = Snapshot(
        snapshot_id=data.snapshot_id,
        created_at=data.created_at,
        payload=data.payload,
    )

    session = SessionState(
        session_id=data.session_id,
        started_at=datetime.utcnow(),
        ended_at=None,
        active=True,
    )

    cursor: ReplicationCursor = replica_engine.apply_snapshot(
        snapshot=snapshot,
        session=session,
    )

    return SnapshotResponse(
        cursor_position=cursor.position,
        cursor_updated_at=cursor.updated_at,
    )