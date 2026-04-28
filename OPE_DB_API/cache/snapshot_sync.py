from typing import List, Dict, Any
from sqlalchemy.orm import Session

from OPE_DB_API.registry import LIVE_TABLE_REGISTRY

# Transport layer (to be implemented later)
from OPE_DB_API.cache.transport import fetch_snapshot_subtree


# ---------------------------------------------------------
# Public entry point
# ---------------------------------------------------------

def sync_domain_snapshot(
    *,
    db: Session,
    code: str,
    domain: str,
    session_id: int,
    root_node_id: int,
) -> None:
    """
    Sync full hierarchy snapshot for a given domain and root node.

    This operation:
    - Fetches authoritative subtree data from server
    - Upserts into local <domain>_data
    - Does NOT affect history cursor
    """
    rows = fetch_snapshot_subtree(
        code=code,
        domain=domain,
        session_id=session_id,
        root_node_id=root_node_id,
    )

    if not rows:
        return

    live_model = LIVE_TABLE_REGISTRY[domain]

    for row in rows:
        existing = db.get(live_model, row["data_id"])
        if existing is None:
            db.add(live_model(**row))
        else:
            existing.node_id = row["node_id"]
            existing.attribute_id = row["attribute_id"]
            existing.value = row["value"]
            db.add(existing)

    db.commit()
# ---------------------------------------------------------
# Server pull
# ---------------------------------------------------------

def fetch_snapshot_from_server(
    domain: str,
    root_node_id: int,
) -> List[Dict[str, Any]]:
    """
    Fetch authoritative subtree snapshot from server.

    Returned rows must include:
    - data_id
    - node_id
    - attribute_id
    - value
    """
    return fetch_snapshot_subtree(
        domain=domain,
        root_node_id=root_node_id,
    )


# ---------------------------------------------------------
# Local upsert logic
# ---------------------------------------------------------

def upsert_snapshot_rows(
    db: Session,
    domain: str,
    rows: List[Dict[str, Any]],
) -> None:
    """
    Upsert snapshot rows into local <domain>_data.
    """
    live_model = LIVE_TABLE_REGISTRY[domain]

    for row in rows:
        data_id = row["data_id"]

        existing = db.get(live_model, data_id)

        if existing is None:
            db.add(live_model(**row))
        else:
            existing.node_id = row["node_id"]
            existing.attribute_id = row["attribute_id"]
            existing.value = row["value"]
            db.add(existing)

    db.commit()
