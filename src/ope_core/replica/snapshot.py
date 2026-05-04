"""
Replica Snapshot Application

This module defines the core logic for applying a Snapshot
to a client-side replica.

The responsibility of this module is to coordinate snapshot
application semantics, not persistence.

Persistence (database writes) must be delegated to
infrastructure adapters.
"""

from typing import Protocol

from ope_core.domain.snapshot import Snapshot
from ope_core.domain.session import SessionState
from ope_core.domain.cursor import ReplicationCursor
from ope_core.domain.errors import InactiveSessionError

class SnapshotApplier(Protocol):
    """
    Protocol for snapshot persistence adapters.

    Implementations of this protocol are responsible for
    materializing snapshot data into the replica storage
    (e.g. PostgreSQL, SQLite, etc.).
    """

    def reset_replica(self) -> None:
        """
        Reset replica state before applying a snapshot.
        """
        ...

    def apply_snapshot_payload(self, snapshot: Snapshot) -> None:
        """
        Persist snapshot payload into the replica.
        """
        ...

    def reset_cursor(self) -> ReplicationCursor:
        """
        Reset replication cursor after snapshot application.
        """
        ...


def apply_snapshot(
    *,
    snapshot: Snapshot,
    session: SessionState,
    applier: SnapshotApplier,
) -> ReplicationCursor:
    """
    Apply a snapshot within a replication session.

    Steps:
    1. Validate session state
    2. Reset replica state
    3. Apply snapshot payload
    4. Reset replication cursor

    Returns:
        ReplicationCursor representing the new baseline state

    Raises:
        ValueError: if session is not active
    """

    if not session.active:
        raise InactiveSessionError(
            "Cannot apply snapshot in inactive session"
        )

    # Step 1: Reset replica state
    applier.reset_replica()

    # Step 2: Apply snapshot data
    applier.apply_snapshot_payload(snapshot)

    # Step 3: Reset cursor to baseline
    cursor = applier.reset_cursor()

    return cursor