"""
Database infrastructure layer for ope_db_api.

This package contains only low-level database primitives:
- SQLAlchemy base
- Engine factory
- Session management

No domain or business logic lives here.
"""

from .base import Base
from .engine import get_engine, get_client_engine
from .session import get_db_session

__all__ = [
    "Base",
    "get_engine",
    "get_db_session",
    "get_client_engine",
]