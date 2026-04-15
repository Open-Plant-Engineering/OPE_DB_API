from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from OPE_DB_API.api.dependencies import db_session
from OPE_DB_API.api.helpers import validate_domain
from OPE_DB_API.crud.commit.commit import commit_session

router = APIRouter(
    prefix="/{code}/{domain}/commit",
    tags=["Commit Operations"],
)


@router.post("/{session_id}")
def api_commit_session(
    code: str,
    domain: str,
    session_id: int,
    db: Session = Depends(db_session),
):
    validate_domain(domain)
    commit_session(
        db,
        domain=domain,
        session_id=session_id,
    )
    return {
        "status": "committed",
        "session_id": session_id,
        "domain": domain,
    }