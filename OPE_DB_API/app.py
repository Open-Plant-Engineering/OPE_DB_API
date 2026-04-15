from fastapi import FastAPI

from OPE_DB_API.api import (
    session_router,
    overlay_router,
    commit_router,
)


def create_app() -> FastAPI:
    """
    Create and return a FastAPI application instance.

    This function is intentionally lightweight and side-effect free.
    All configuration, routing, database wiring, and middleware
    will be attached in later steps.
    """
    app = FastAPI(
        title="OPE DB API",
        description="Session-based database data management service",
        version="0.1.0",
    )
    
    app.include_router(session_router)
    app.include_router(overlay_router)
    app.include_router(commit_router)

    return app