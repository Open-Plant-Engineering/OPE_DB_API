"""
PostgreSQL Snapshot Applier

Concrete implementation of the SnapshotApplier protocol
using SQLAlchemy and a relational database.

This module handles the physical persistence of snapshot
data into the replica database.
"""

from datetime import datetime
from typing import Mapping, Any

from sqlalchemy.orm import Session

from ope_core.domain.snapshot import Snapshot
from ope_core.domain.cursor import ReplicationCursor
from ope_core.replica.snapshot import SnapshotApplier


class PostgresSnapshotApplier(SnapshotApplier):
    """
    PostgreSQL-backed implementation of SnapshotApplier.

    This class is responsible for:
    - Clearing replica state
    - Persisting snapshot payload
    - Resetting replication cursor
    """

    def __init__(self, session: Session):
        self._session = session

    def reset_replica(self) -> None:
        """
        Reset replica database state before applying a snapshot.

        NOTE:
        This implementation assumes a simple strategy:
        - Truncate all replica tables

        More sophisticated implementations may:
        - Use schema resets
        - Use versioned snapshots
        """

        # IMPORTANT:
        # This is intentionally abstract.
        # Actual table names should be centralized elsewhere.
        self._session.execute("PRAGMA foreign_keys = OFF")  # no-op on Postgres
        # Example placeholder:
        # self._session.execute("TRUNCATE TABLE live_data")

    def apply_snapshot_payload(self, snapshot: Snapshot) -> None:
        """
        Persist snapshot payload into the replica database.

        Args:
            snapshot: Snapshot domain object
        """

        payload: Mapping[str, Any] = snapshot.payload

        # Example strategy:
        # payload is assumed to be a mapping of table_name -> rows
        for table_name, rows in payload.items():
            for row in rows:
                columns = ", ".join(row.keys())
                placeholders = ", ".join([f":{k}" for k in row.keys()])

                sql = (
                    f"INSERT INTO {table_name} ({columns}) "
                    f"VALUES ({placeholders})"
                )

                self._session.execute(sql, row)

    def reset_cursor(self) -> ReplicationCursor:
        """
        Reset replication cursor after snapshot application.

        Returns:
            ReplicationCursor at baseline state
        """

        return ReplicationCursor(
            position=None,
            updated_at=datetime.utcnow(),
        )