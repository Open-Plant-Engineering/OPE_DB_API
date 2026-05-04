"""
PostgreSQL History Applier

Concrete implementation of the HistoryApplier protocol
using SQLAlchemy and a relational database.

This module applies incremental history changes to the
replica database and advances the replication cursor.
"""

from datetime import datetime
from typing import Any, Mapping

from sqlalchemy.orm import Session

from ope_core.domain.history import HistoryBatch
from ope_core.domain.cursor import ReplicationCursor
from ope_core.replica.history import HistoryApplier


class PostgresHistoryApplier(HistoryApplier):
    """
    PostgreSQL-backed implementation of HistoryApplier.

    Responsibilities:
    - Apply incremental history changes
    - Advance replication cursor deterministically
    """

    def __init__(self, session: Session):
        self._session = session

    def apply_history_changes(self, history: HistoryBatch) -> None:
        """
        Apply incremental history changes to replica storage.

        Assumes:
        - history.changes is an ordered sequence
        - each change is a mapping with at least:
            - operation (INSERT / UPDATE / DELETE)
            - table
            - data
        """

        for change in history.changes:
            self._apply_single_change(change)

    def _apply_single_change(self, change: Mapping[str, Any]) -> None:
        """
        Apply a single change operation.

        Expected change format:
        {
            "op": "INSERT" | "UPDATE" | "DELETE",
            "table": "table_name",
            "data": {...},
            "where": {...}  # for UPDATE / DELETE
        }
        """

        op = change["op"].upper()
        table = change["table"]

        if op == "INSERT":
            data = change["data"]
            self._insert_row(table, data)

        elif op == "UPDATE":
            data = change["data"]
            where = change["where"]
            self._update_row(table, data, where)

        elif op == "DELETE":
            where = change["where"]
            self._delete_row(table, where)

        else:
            raise ValueError(f"Unsupported history operation: {op}")

    def _insert_row(self, table: str, data: Mapping[str, Any]) -> None:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f":{k}" for k in data.keys())

        sql = (
            f"INSERT INTO {table} ({columns}) "
            f"VALUES ({placeholders})"
        )

        self._session.execute(sql, data)

    def _update_row(
        self,
        table: str,
        data: Mapping[str, Any],
        where: Mapping[str, Any],
    ) -> None:
        set_clause = ", ".join(f"{k} = :set_{k}" for k in data.keys())
        where_clause = " AND ".join(f"{k} = :where_{k}" for k in where.keys())

        params = {
            **{f"set_{k}": v for k, v in data.items()},
            **{f"where_{k}": v for k, v in where.items()},
        }

        sql = (
            f"UPDATE {table} SET {set_clause} "
            f"WHERE {where_clause}"
        )

        self._session.execute(sql, params)

    def _delete_row(self, table: str, where: Mapping[str, Any]) -> None:
        where_clause = " AND ".join(f"{k} = :{k}" for k in where.keys())

        sql = f"DELETE FROM {table} WHERE {where_clause}"

        self._session.execute(sql, where)

    def advance_cursor(self, history: HistoryBatch) -> ReplicationCursor:
        """
        Advance replication cursor to reflect applied history batch.

        Cursor position uses history.batch_id to ensure
        strict monotonic progression.
        """

        return ReplicationCursor(
            position=history.batch_id,
            updated_at=datetime.utcnow(),
        )