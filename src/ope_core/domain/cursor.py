"""
Replication Cursor Domain Object

A ReplicationCursor represents the current position of a client replica
within the authoritative replication stream.

It is used to ensure:
- deterministic history replay
- idempotent synchronization
- resumable replication

Invariants:
- Cursors must advance monotonically
- Cursors must never move backwards
- Applying a snapshot resets cursor state
- Cursor state must be persisted atomically with history replay
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ReplicationCursor:
    """
    Immutable representation of a replication cursor.

    Attributes:
        position: Monotonic replication position (timestamp, sequence, or ID)
        updated_at: Timestamp when the cursor was last advanced
    """

    position: Optional[str]
    updated_at: Optional[datetime]