from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from OPE_DB_API.api.dependencies import db_session
from OPE_DB_API.api.helpers import validate_domain
from OPE_DB_API.schemas.work import WorkPushRequest
from OPE_DB_API.crud.session import get_active_session
from OPE_DB_API.crud.work.push import push_work
from OPE_DB_API.crud.commit.commit import commit_session
from OPE_DB_API.crud.session import get_active_session
from OPE_DB_API.crud.session.abort import abort_session
from OPE_DB_API.crud.work.read import read_current_work
from OPE_DB_API.crud.session import get_active_session

from OPE_DB_API.registry import (
    LIVE_TABLE_REGISTRY,
    OVERLAY_TABLE_REGISTRY,
)

router = APIRouter(
    prefix="/work",
    tags=["Workflows"],
)

@router.post("/push")
def api_push_work(
    code: str,
    domain: str,
    payload: WorkPushRequest,
    db: Session = Depends(db_session),
):
    validate_domain(domain)

    session = get_active_session(db)
    if not session:
        # reuse existing behavior (no new errors yet)
        raise RuntimeError("No active session")

    row = push_work(
        db,
        domain=domain,
        session_id=session.session_id,
        payload=payload,
    )

    db.commit()
    return {
        "status": "staged",
        "data_id": row.data_id,
    }


@router.post("/save")
def api_save_work(
    code: str,
    domain: str,
    db: Session = Depends(db_session),
):
    validate_domain(domain)

    session = get_active_session(db)
    if not session:
        raise HTTPException(status_code=409, detail="No active session")

    # Atomic save
    with db.begin():
        commit_session(
            db=db,
            domain=domain,
            session_id=session.session_id,
        )

    return {
        "status": "saved",
        "session_id": session.session_id,
        "domain": domain,
    }


@router.post("/discard")
def api_discard_work(
    code: str,
    domain: str,
    db: Session = Depends(db_session),
):
    validate_domain(domain)

    session = get_active_session(db)
    if not session:
        raise HTTPException(status_code=409, detail="No active session")

    with db.begin():
        abort_session(
            db=db,
            session_id=session.session_id,
            domain=domain,
        )

    return {
        "status": "discarded",
        "session_id": session.session_id,
        "domain": domain,
    }


@router.get("")
def api_get_current_work(
    code: str,
    domain: str,
    db: Session = Depends(db_session),
):
    validate_domain(domain)

    session = get_active_session(db)
    if not session:
        # no active session → show latest committed state
        Live = LIVE_TABLE_REGISTRY[domain]
        return db.query(Live).all()

    return read_current_work(
        db,
        domain=domain,
        session_id=session.session_id,
    )