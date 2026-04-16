from fastapi import HTTPException
from OPE_DB_API.errors import SessionNotActiveError

def handle_domain_error(exc: Exception):
    if isinstance(exc, SessionNotActiveError):
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )
    raise exc