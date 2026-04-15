"""
Registry layer for ope_db_api.

Defines which tables and columns are allowed to be
accessed by generic APIs.
"""

from .tables import (
    LIVE_TABLE_REGISTRY,
    OVERLAY_TABLE_REGISTRY,
    HISTORY_TABLE_REGISTRY,
)

from .search import SEARCHABLE_COLUMN_REGISTRY

__all__ = [
    "LIVE_TABLE_REGISTRY",
    "OVERLAY_TABLE_REGISTRY",
    "HISTORY_TABLE_REGISTRY",
    "SEARCHABLE_COLUMN_REGISTRY",
]