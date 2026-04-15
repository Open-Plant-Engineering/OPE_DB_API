"""
OPE_DB_API

Session-based JSONB editing and query engine
(CAD / PLM style workflow).
"""
from .metadata import __version__

from .main import create_app
from .api.jsonb_api import router as jsonb_router
from .api.session_api import router as session_router

__all__ = [
    "create_app",
    "jsonb_router",
    "session_router",
]