from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from OPE_DB_API.api.dependencies import db_session
from OPE_DB_API.api.helpers import validate_domain
from OPE_DB_API.crud.commit.commit import commit_session

router = APIRouter(
    prefix="/{code}/commit",
    tags=["Commit Operations"],
)


@router.post("/{session_id}")
def api_commit_session(
    code: str,
    session_id: int,
    db: Session = Depends(db_session),
):
    validate_domain(code)
    commit_session(
        db,
        domain=code,
        session_id=session_id,
    )
    return {
        "status": "committed",
        "session_id": session_id,
        "domain": code,
    }