from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from OPE_DB_API.api.dependencies import db_session
from OPE_DB_API.api.helpers import validate_domain
from OPE_DB_API.schemas.work import WorkPushRequest, BulkWorkPushRequest

from OPE_DB_API.crud.session import validate_session_active
from OPE_DB_API.crud.work.push import push_work
from OPE_DB_API.crud.work.read import read_current_work
from OPE_DB_API.crud.commit.commit import commit_session
from OPE_DB_API.crud.session.abort import abort_session
from OPE_DB_API.crud.work.push_bulk import push_work_bulk

from OPE_DB_API.registry import LIVE_TABLE_REGISTRY

router = APIRouter(
    prefix="/{code}/{domain}/{session_id}/work",
    tags=["Workflows"],
)

# ---------------------------------------------------------
# PUSH (Stage work into overlay bucket)
# ---------------------------------------------------------
@router.post("/push")
def api_push_work(
    code: str,
    domain: str,
    session_id: int,
    payload: WorkPushRequest,
    db: Session = Depends(db_session),
):
    validate_domain(domain)

    validate_session_active(db, session_id=session_id)
    
    try:
        row = push_work(
            db=db,
            domain=domain,
            session_id=session_id,
            payload=payload,
        )
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
    return {
        "status": "staged",
        "data_id": row.data_id,
    }


# ---------------------------------------------------------
# SAVE (Commit work)
# ---------------------------------------------------------
@router.post("/commit")
def api_commit_work(
    code: str,
    domain: str,
    session_id: int,
    db: Session = Depends(db_session),
):
    validate_domain(domain)

    validate_session_active(db, session_id=session_id)
    
    try:
        commit_session(
            db=db,
            domain=domain,
            session_id=session_id,
        )
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return {
        "status": "saved",
        "session_id": session_id,
    }


# ---------------------------------------------------------
# DISCARD (Abort work)
# ---------------------------------------------------------
@router.post("/discard")
def api_discard_work(
    code: str,
    domain: str,
    session_id: int,
    db: Session = Depends(db_session),
):
    validate_domain(domain)

    validate_session_active(db, session_id=session_id)
    try:
        abort_session(
            db=db,
            session_id=session_id,
            domain=domain,
        )
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
    return {
        "status": "discarded",
        "session_id": session_id,
    }


# ---------------------------------------------------------
# READ CURRENT WORK (Live ⊕ Overlay)
# ---------------------------------------------------------
@router.get("")
def api_get_current_work(
    code: str,
    domain: str,
    session_id: int,
    db: Session = Depends(db_session),
):
    validate_domain(domain)

    validate_session_active(db, session_id=session_id)
    
    return read_current_work(
        db=db,
        domain=domain,
        session_id=session_id,
    )


# ---------------------------------------------------------
# Bulk Push WORK (Stage work into overlay bucket)
# ---------------------------------------------------------
@router.post("/push/bulk")
def api_push_work_bulk(
    code: str,
    domain: str,
    session_id: int,
    payload: BulkWorkPushRequest,
    db: Session = Depends(db_session),
):
    validate_domain(domain)

    validate_session_active(db, session_id=session_id)

    success, failure = push_work_bulk(
        db=db,
        domain=domain,
        session_id=session_id,
        items=payload.items,
    )

    db.commit()

    return {
        "status": (
            "partial_success" if success and failure
            else "success" if success
            else "failure"
        ),
        "success": success,
        "failure": failure,
    }
