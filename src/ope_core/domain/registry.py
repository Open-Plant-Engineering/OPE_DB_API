"""
Registry Domain Object

RegistryEntry represents a domain or table that is registered
for synchronization and replication within the OPE platform.

The registry defines *what* is tracked, not *how* it is stored.

Invariants:
- Registry entries are immutable
- Registry entries uniquely identify a tracked domain/table
- Only registered entries participate in snapshot and history flows
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RegistryEntry:
    """
    Immutable representation of a registered domain or table.

    Attributes:
        name: Logical name of the registered entity (domain/table)
        schema: Optional schema name (for database-backed entries)
        description: Optional human-readable description
        enabled: Whether this entry is currently active for replication
    """

    name: str
    schema: Optional[str]
    description: Optional[str]
    enabled: bool