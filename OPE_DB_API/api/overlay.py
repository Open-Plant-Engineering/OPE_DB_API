from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from OPE_DB_API.api.dependencies import db_session
from OPE_DB_API.api.helpers import validate_domain
from OPE_DB_API.crud.overlay import (
    stage_create,
    stage_update,
    stage_delete,
    read_overlay_by_session,
)

router = APIRouter(
    prefix="/{code}/{domain}/overlay",
    tags=["Overlay Operations"],
)


@router.post("/create")
def api_stage_create(
    code: str,
    domain: str,
    payload: dict,
    db: Session = Depends(db_session),
):
    validate_domain(domain)
    row = stage_create(db, domain, payload)
    db.commit()
    db.refresh(row)
    return row



@router.put("/update/{overlay_id}")
def api_stage_update(
    code: str,
    domain: str,
    overlay_id: int,
    value,
    db: Session = Depends(db_session),
):
    validate_domain(domain)
    row = stage_update(db, domain, overlay_id, value)
    db.commit()
    return row


@router.delete("/delete/{overlay_id}")
def api_stage_delete(
    code: str,
    domain: str,
    overlay_id: int,
    db: Session = Depends(db_session),
):
    validate_domain(domain)
    row = stage_delete(db, domain, overlay_id)
    db.commit()
    return {"status": "staged_delete", "overlay_id": overlay_id}


@router.get("/{session_id}")
def api_read_overlay(
    code: str,
    domain: str,
    session_id: int,
    db: Session = Depends(db_session),
):
    validate_domain(domain)
    return read_overlay_by_session(db, domain, session_id)
