from sqlalchemy.orm import Session
from typing import Set

from OPE_DB_API.registry import LIVE_TABLE_REGISTRY


# ---------------------------------------------------------
# Public entry point
# ---------------------------------------------------------

def clear_domain_node_cache(
    db: Session,
    domain: str,
    root_node_id: int,
) -> None:
    """
    Remove all locally cached data for a node and its hierarchy
    from <domain>_data.

    This operation:
    - Is local-only
    - Does not affect history
    - Does not reset cursor
    """
    live_model = LIVE_TABLE_REGISTRY[domain]

    node_ids = _collect_subtree_node_ids(
        db=db,
        live_model=live_model,
        root_node_id=root_node_id,
    )

    if not node_ids:
        return

    (
        db.query(live_model)
        .filter(live_model.node_id.in_(node_ids))
        .delete(synchronize_session=False)
    )

    db.commit()


# ---------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------

def _collect_subtree_node_ids(
    db: Session,
    live_model,
    root_node_id: int,
) -> Set[int]:
    """
    Collect all node_ids belonging to the cached subtree.

    NOTE:
    This relies purely on local cached data.
    """
    node_ids = set()
    stack = [root_node_id]

    while stack:
        current = stack.pop()
        if current in node_ids:
            continue

        node_ids.add(current)

        # Find children by scanning cached data
        child_nodes = (
            db.query(live_model.node_id)
            .filter(live_model.node_id != current)
            .all()
        )

        for (child_id,) in child_nodes:
            if child_id not in node_ids:
                stack.append(child_id)

    return node_ids
