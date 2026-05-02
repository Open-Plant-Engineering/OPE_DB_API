from sqlalchemy.orm import Session
from sqlalchemy import cast
from sqlalchemy.types import BigInteger
from typing import Set, List

from OPE_DB_API.registry import LIVE_TABLE_REGISTRY


def fetch_snapshot_subtree(
    db: Session,
    domain: str,
    root_node_id: int,
    owner_attribute_id: int,
) -> List:
    """
    Fetch authoritative subtree snapshot.

    Subtree definition:
    A node belongs to the subtree if it is reachable from root_node_id
    via repeated Owner-attribute relationships.
    """

    model = LIVE_TABLE_REGISTRY[domain]

    # -------------------------------------------------
    # 1️⃣ Collect all node_ids in the subtree
    # -------------------------------------------------
    to_visit = {root_node_id}
    all_nodes: Set[int] = set()

    while to_visit:
        current = to_visit.pop()

        if current in all_nodes:
            continue

        all_nodes.add(current)

        # Find children where:
        # attribute_id == Owner AND value == current node_id
        children = (
            db.query(model.node_id)
            .filter(
                model.attribute_id == owner_attribute_id,
                cast(model.value, BigInteger) == current,
            )
            .all()
        )

        for (child_id,) in children:
            if child_id not in all_nodes:
                to_visit.add(child_id)

    # -------------------------------------------------
    # 2️⃣ Return ALL LIVE rows for the subtree
    # -------------------------------------------------
    return (
        db.query(model)
        .filter(model.node_id.in_(all_nodes))
        .all()
    )