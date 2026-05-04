"""
Replica History Replay

This module defines the core logic for applying HistoryBatch
objects to a client-side replica.

History replay advances replica state deterministically using
authoritative incremental changes.

Persistence and cursor storage are delegated to adapter protocols.
"""

from typing import Protocol

from ope_core.domain.history import HistoryBatch
from ope_core.domain.session import SessionState
from ope_core.domain.cursor import ReplicationCursor


class HistoryApplier(Protocol):
    """
    Protocol for history persistence adapters.

    Implementations of this protocol are responsible for:
    - Applying history changes to replica storage
    - Advancing and persisting the replication cursor
    """

    def apply_history_changes(self, history: HistoryBatch) -> None:
        """
        Persist history changes into the replica.
        """
        ...

    def advance_cursor(self, history: HistoryBatch) -> ReplicationCursor:
        """
        Advance and persist the replication cursor.

        Returns:
            Updated ReplicationCursor
        """
        ...


def apply_history(
    *,
    history: HistoryBatch,
    session: SessionState,
    current_cursor: ReplicationCursor,
    applier: HistoryApplier,
) -> ReplicationCursor:
    """
    Apply a history batch within an active replication session.

    Steps:
    1. Validate session
    2. Apply history changes
    3. Advance replication cursor

    Returns:
        Updated ReplicationCursor

    Raises:
        ValueError: if session is inactive
        ValueError: if cursor state is invalid
    """

    if not session.active:
        raise ValueError("Cannot apply history in inactive session")

    if current_cursor.position is None:
        raise ValueError(
            "Cannot apply history before snapshot has been applied"
        )

    # Step 1: Apply history changes to replica
    applier.apply_history_changes(history)

    # Step 2: Advance cursor deterministically
    new_cursor = applier.advance_cursor(history)

    return new_cursor