from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from OPE_DB_API.api.dependencies import db_session
from OPE_DB_API.api.helpers import validate_domain
from OPE_DB_API.schemas.search import SearchRequest
from OPE_DB_API.crud.search.executor import execute_search
from OPE_DB_API.crud.session import validate_session_active

router = APIRouter(
    prefix="/{code}/{domain}/{session_id}/search",
    tags=["Search"],
)


@router.post("")
def api_search(
    code: str,
    domain: str,
    session_id: int,
    payload: SearchRequest,
    db: Session = Depends(db_session),
):
    validate_domain(domain)

    validate_session_active(db, session_id=session_id)

    result = execute_search(
        db=db,
        domain=domain,
        session_id=session_id,
        search=payload,
    )

    return result