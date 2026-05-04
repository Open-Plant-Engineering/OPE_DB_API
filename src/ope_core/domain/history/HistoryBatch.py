"""
History Domain Object

A HistoryBatch represents an ordered set of authoritative changes
that advance replica state after a snapshot has been applied.

History batches are applied sequentially to ensure deterministic
replica advancement.

Invariants:
- History batches are immutable
- History batches must be applied in strict order
- History replay must occur only after a snapshot is applied
- History batches represent incremental state changes
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Sequence


@dataclass(frozen=True)
class HistoryBatch:
    """
    Immutable representation of a batch of incremental changes.

    Attributes:
        batch_id: Unique identifier for this history batch
        created_at: Timestamp when this batch was generated
        changes: Ordered list of change records
    """

    batch_id: str
    created_at: datetime
    changes: Sequence[Any]