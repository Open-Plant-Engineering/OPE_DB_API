"""
Snapshot Domain Object

A Snapshot represents a complete, authoritative view of server-side
state at a specific point in time.

Snapshots are used to initialize client replicas and establish a
replication baseline.

Invariants:
- Snapshots are immutable once created
- A snapshot must be applied before any history replay
- Snapshots represent authoritative state (not incremental changes)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping


@dataclass(frozen=True)
class Snapshot:
    """
    Immutable representation of a server snapshot.

    Attributes:
        snapshot_id: Unique identifier of the snapshot
        created_at: Timestamp when snapshot was generated
        payload: Arbitrary structured data representing full state
    """

    snapshot_id: str
    created_at: datetime
    payload: Mapping[str, Any]