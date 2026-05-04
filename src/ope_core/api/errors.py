"""
API Error Handlers

Maps domain-level errors to appropriate HTTP responses.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ope_core.domain.errors import (
    DomainError,
    InactiveSessionError,
    SnapshotRequiredError,
    InvalidHistoryError,
)


def register_error_handlers(app: FastAPI) -> None:
    """
    Register API error handlers.
    """

    @app.exception_handler(InactiveSessionError)
    async def inactive_session_handler(
        request: Request,
        exc: InactiveSessionError,
    ):
        return JSONResponse(
            status_code=409,
            content={"error": str(exc)},
        )

    @app.exception_handler(SnapshotRequiredError)
    async def snapshot_required_handler(
        request: Request,
        exc: SnapshotRequiredError,
    ):
        return JSONResponse(
            status_code=412,
            content={"error": str(exc)},
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(
        request: Request,
        exc: DomainError,
    ):
        return JSONResponse(
            status_code=400,
            content={"error": str(exc)},
        )