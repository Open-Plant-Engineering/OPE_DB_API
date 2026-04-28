from sqlalchemy.orm import Session
from typing import List

from OPE_DB_API.registry import LIVE_TABLE_REGISTRY


def fetch_snapshot_subtree(
    db: Session,
    domain: str,
    root_node_id: int,
) -> List:
    """
    Fetch authoritative subtree snapshot for a domain and root node.

    NOTE:
    Hierarchy resolution is assumed to be domain-specific
    and already encoded in domain_data structure.
    """
    model = LIVE_TABLE_REGISTRY[domain]

    # Current assumption:
    # Server already stores subtree relationships implicitly
    return (
        db.query(model)
        .filter(model.node_id == root_node_id)
        .all()
    )