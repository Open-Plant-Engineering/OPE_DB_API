"""
Session Domain Object

SessionState represents the logical context in which replication
operations (snapshot application and history replay) occur.

A session provides isolation and ordering guarantees across
synchronization operations.

Invariants:
- A session must exist before applying snapshots or history
- A session has a clear lifecycle: STARTED → ACTIVE → CLOSED
- Cursor advancement must occur within a session
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class SessionState:
    """
    Immutable representation of a replication or working session.

    Attributes:
        session_id: Unique identifier of the session
        started_at: Timestamp when the session started
        ended_at: Timestamp when the session ended (if closed)
        active: Whether the session is currently active
    """

    session_id: str
    started_at: datetime
    ended_at: Optional[datetime]
    active: bool
