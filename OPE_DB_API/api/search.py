from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from OPE_DB_API.api.dependencies import db_session
from OPE_DB_API.api.helpers import validate_domain
from OPE_DB_API.schemas.search import SearchRequest
from OPE_DB_API.crud.search.executor import execute_search

router = APIRouter(
    prefix="/{code}/search",
    tags=["Search"],
)


@router.post("")
def api_search(
    code: str,
    payload: SearchRequest,
    db: Session = Depends(db_session),
):
    validate_domain(code)

    result = execute_search(
        db=db,
        domain=code,
        search=payload,
    )

    return result