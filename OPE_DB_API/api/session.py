from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from OPE_DB_API.api.dependencies import db_session
from OPE_DB_API.crud.session import (
    start_session,
    get_active_session,
    list_sessions,
    close_session,
)

router = APIRouter(
    prefix="/{code}/{domain}/session",
    tags=["Session Management"],
)


@router.post("/start")
def api_start_session(
    code: str,
    domain: str,
    session_id: int,
    username: str | None = None,
    hostname: str | None = None,
    db: Session = Depends(db_session),
):
    ses = start_session(
        db,
        session_id=session_id,
        username=username,
        hostname=hostname,
        domain=domain,
    )
    db.commit()
    db.refresh(ses)
    return ses


@router.get("/active")
def api_get_active_session(
    code: str,
    username: str | None = Query(default=None),
    hostname: str | None = Query(default=None),
    db: Session = Depends(db_session),
):
    return get_active_session(
        db,
        username=username,
        hostname=hostname,
    )


@router.get("")
def api_list_sessions(
    code: str,
    username: str | None = None,
    hostname: str | None = None,
    active_only: bool = False,
    db: Session = Depends(db_session),
):
    return list_sessions(
        db,
        username=username,
        hostname=hostname,
        active_only=active_only,
    )


@router.post("/{session_id}/close")
def api_close_session(
    code: str,
    session_id: int,
    db: Session = Depends(db_session),
):
    ses = close_session(db, session_id=session_id)
    db.commit()
    return ses