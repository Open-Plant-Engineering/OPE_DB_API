from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from OPE_DB_API.api.dependencies import db_session
from OPE_DB_API.api.helpers import validate_domain
from OPE_DB_API.schemas.work import WorkPushRequest
from OPE_DB_API.crud.session import get_active_session
from OPE_DB_API.crud.work.push import push_work

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
