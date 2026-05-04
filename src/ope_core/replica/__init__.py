"""
Replica Layer Package

The replica layer implements client-side replication behavior.
It is responsible for:

- Applying snapshots to initialize local state
- Replaying history batches to advance replica state
- Managing replication cursor state
- Coordinating replication sessions

Rules:
- Replica code may depend on ope_core.domain
- Replica code may depend on infrastructure adaptation layers
- Replica code must NOT redefine domain concepts
- Replica code must NOT expose SQL or ORM details directly to callers
"""

__all__ = []