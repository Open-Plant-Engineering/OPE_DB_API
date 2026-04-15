from fastapi import FastAPI


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

    return app