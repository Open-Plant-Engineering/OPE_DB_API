from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from OPE_DB_API.api.dependencies import db_session
from OPE_DB_API.api.helpers import validate_domain
from OPE_DB_API.crud.session import validate_session_active

from OPE_DB_API.crud.sync.history import fetch_history_after
from OPE_DB_API.crud.sync.snapshot import fetch_snapshot_subtree


router = APIRouter(
    prefix="/{code}/{domain}/{session_id}/sync",
    tags=["Sync"],
)

# ---------------------------------------------------------
# History Sync API
# ---------------------------------------------------------

@router.get("/history")
def api_sync_history(
    code: str,
    domain: str,
    session_id: int,
    after_history_id: Optional[int] = Query(default=None),
    limit: int = Query(default=5000),
    db: Session = Depends(db_session),
):
    """
    Return committed history rows after a given cursor.
    """
    validate_domain(domain)
    validate_session_active(db, session_id=session_id)

    rows = fetch_history_after(
        db=db,
        domain=domain,
        after_history_id=after_history_id,
        limit=limit,
    )
    return rows


# ---------------------------------------------------------
# Snapshot Sync API
# ---------------------------------------------------------

@router.get("/snapshot")
def api_sync_snapshot(
    code: str,
    domain: str,
    session_id: int,
    root_node_id: int,
    db: Session = Depends(db_session),
):
    """
    Return authoritative subtree snapshot for GetCurrentNodeHierarchy.
    """
    validate_domain(domain)
    validate_session_active(db, session_id=session_id)

    rows = fetch_snapshot_subtree(
        db=db,
        domain=domain,
        root_node_id=root_node_id,
    )
    return rows