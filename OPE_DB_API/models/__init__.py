"""
Core ORM model abstractions for ope_db_api.

These models define the semantic roles of data in the system:
- live data
- overlay (draft) data
- history (audit) data
- session metadata

IDENTITY RULE:
- data_id uniquely identifies a single attribute globally
- DbDataOverlayBase shadows DbDataBase by data_id
- DbDataHistoryBase records mutations by data_id
- There is no separate overlay identity
"""

from .db_data import DbDataBase
from .db_data_overlay import DbDataOverlayBase
from .db_data_history import DbDataHistoryBase
from .session import SessionMetadata

__all__ = [
    "DbDataBase",
    "DbDataOverlayBase",
    "DbDataHistoryBase",
    "SessionMetadata",
]