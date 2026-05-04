"""
FastAPI Application Factory

This module defines the FastAPI application object for OPE Core.

Responsibilities:
- Create FastAPI app
- Configure global dependencies
- Register routers

Business logic must NOT be implemented here.
"""

from fastapi import FastAPI

from ope_core.replica.engine import ReplicaEngine
from ope_core.api.errors import register_error_handlers

def create_app(*, database_url: str) -> FastAPI:
    """
    Application factory.

    Args:
        database_url: Database URL passed to ReplicaEngine

    Returns:
        Configured FastAPI application
    """

    app = FastAPI(
        title="OPE Core API",
        version="0.1.0",
        description="Replication and snapshot API for OPE Core platform",
    )

    register_error_handlers(app)
    
    # --- Core Dependencies -------------------------------------------------

    replica_engine = ReplicaEngine(database_url)

    # Store shared objects on app state
    app.state.replica_engine = replica_engine

    # Routers will be registered here in future steps
    # Example:
    from ope_core.api.routers.snapshot import router as snapshot_router
    app.include_router(snapshot_router)
    from ope_core.api.routers.history import router as history_router
    app.include_router(history_router)

   
    return app
