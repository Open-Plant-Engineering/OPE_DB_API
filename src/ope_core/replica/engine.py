"""
Replica Engine (Composition Root)

This module wires together:
- database infrastructure
- replica orchestration logic
- concrete persistence adapters

This is the ONLY place where infrastructure and replica logic meet.
"""

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ope_core.domain.snapshot import Snapshot
from ope_core.domain.history import HistoryBatch
from ope_core.domain.session import SessionState
from ope_core.domain.cursor import ReplicationCursor

from ope_core.replica.snapshot import apply_snapshot
from ope_core.replica.history import apply_history

from ope_core.infrastructure.db.snapshot_applier import (
    PostgresSnapshotApplier,
)
from ope_core.infrastructure.db.history_applier import (
    PostgresHistoryApplier,
)
from ope_core.infrastructure.db.engine import (
    create_db_engine,
    create_session_factory,
    db_session,
)


class ReplicaEngine:
    """
    High-level entry point for replica operations.

    Dependent projects should interact with THIS class,
    not with individual adapters or DB sessions.
    """

    def __init__(self, database_url: str):
        self._engine: Engine = create_db_engine(database_url)
        self._session_factory: sessionmaker = create_session_factory(
            self._engine
        )

    def apply_snapshot(
        self,
        *,
        snapshot: Snapshot,
        session: SessionState,
    ) -> ReplicationCursor:
        """
        Apply a snapshot to the local replica.

        Returns:
            ReplicationCursor representing baseline state
        """
        with db_session(self._session_factory) as db:
            applier = PostgresSnapshotApplier(db)
            return apply_snapshot(
                snapshot=snapshot,
                session=session,
                applier=applier,
            )

    def apply_history(
        self,
        *,
        history: HistoryBatch,
        session: SessionState,
        current_cursor: ReplicationCursor,
    ) -> ReplicationCursor:
        """
        Apply a history batch to the local replica.

        Returns:
            Updated ReplicationCursor
        """
        with db_session(self._session_factory) as db:
            applier = PostgresHistoryApplier(db)
            return apply_history(
                history=history,
                session=session,
                current_cursor=current_cursor,
                applier=applier,
            )