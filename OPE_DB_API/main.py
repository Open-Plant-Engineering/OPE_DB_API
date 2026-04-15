from fastapi import FastAPI
from OPE_DB_API.metadata import __version__, __api_title__
# from OPE_DB_API.api.jsonb_api import router as jsonb_router
# from OPE_DB_API.api.session_api import router as session_router
# from OPE_DB_API.api.search_api import router as search_router

def create_app() -> FastAPI:
    """
    Application bootstrap.

    IMPORTANT:
    - No global engine
    - No Base.metadata.create_all()
    - DB setup happens inside get_engine(code)
    """
    app = FastAPI(
        title=__api_title__,
        version=__version__,
    )

    # Register JSONB dynamic API
    # app.include_router(jsonb_router)
    # app.include_router(session_router)
    # app.include_router(search_router)

    return app

app = create_app()