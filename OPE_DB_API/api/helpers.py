from fastapi import HTTPException

from OPE_DB_API.registry import LIVE_TABLE_REGISTRY


def validate_domain(domain: str):
    """
    Validate that the domain is registered.
    """
    if domain not in LIVE_TABLE_REGISTRY:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid domain: {domain}",
        )