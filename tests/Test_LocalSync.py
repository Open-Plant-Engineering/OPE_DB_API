"""
Manual local cache test (no pytest required).

Run:
    python test_local_manual.py
"""

from pprint import pprint

from OPE_DB_API.db.engine import get_client_config
from OPE_DB_API.db.session import get_db_session
from OPE_DB_API.cache.engine import CacheEngine
from OPE_DB_API.registry import LIVE_TABLE_REGISTRY
import OPE_DB_API.cache.transport as transport
from OPE_DB_API.db.init_db import init_database

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

CODE = "XYZ"
DOMAIN = "DESI"
SESSION_ID = 9999
ROOT_NODE_ID = 10


# -------------------------------------------------------------------
# Monkey-patch transport layer (fake server)
# -------------------------------------------------------------------

def fake_fetch_history_batch(
    *,
    code,
    domain,
    session_id,
    after_history_id,
    limit=5000,
):
    print("\n[SERVER] fetch_history_batch called")
    return [
        {
            "history_id": 1,
            "data_id": 1001,
            "session_id": session_id,
            "operation_type": 1,  # CREATE
            "old_value": None,
            "new_value": {
                "node_id": 10,
                "attribute_id": 1,
                "value": {"name": "Pump A"},
            },
        },
        {
            "history_id": 2,
            "data_id": 1001,
            "session_id": session_id,
            "operation_type": 2,  # UPDATE
            "old_value": {"name": "Pump A"},
            "new_value": {
                "node_id": 10,
                "attribute_id": 1,
                "value": {"name": "Pump A1"},
            },
        },
        {
            "history_id": 3,
            "data_id": 1002,
            "session_id": session_id,
            "operation_type": 1,  # CREATE
            "old_value": None,
            "new_value": {
                "node_id": 10,
                "attribute_id": 2,
                "value": {"power": 5},
            },
        },
    ]


def fake_fetch_snapshot_subtree(
    *,
    code,
    domain,
    session_id,
    root_node_id,
):
    print("\n[SERVER] fetch_snapshot_subtree called")
    return [
        {
            "data_id": 2001,
            "node_id": root_node_id,
            "attribute_id": 99,
            "value": {"snapshot": True},
        }
    ]


transport.fetch_history_batch = fake_fetch_history_batch
transport.fetch_snapshot_subtree = fake_fetch_snapshot_subtree


# -------------------------------------------------------------------
# Helper: print live table
# -------------------------------------------------------------------

def print_live_table(db):
    model = LIVE_TABLE_REGISTRY[DOMAIN]
    rows = db.query(model).order_by(model.data_id).all()

    print(f"\n[LIVE TABLE] {DOMAIN}_data ({len(rows)} rows)")
    for r in rows:
        print(
            f" data_id={r.data_id}, node_id={r.node_id}, "
            f"attribute_id={r.attribute_id}, value={r.value}"
        )


# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------

def main():
    print("\n=== LOCAL CACHE MANUAL TEST START ===")

    # Step 1: prepare local DB
    engine = get_client_config(CODE)
    init_database(engine)

    with get_db_session(CODE) as db:
        engine_cache = CacheEngine(
            db=db,
            code=CODE,
            session_id=SESSION_ID,
        )

        # -------------------------------------------------------------
        # Step 2: history sync
        # -------------------------------------------------------------
        print("\n>>> STEP 1: History Sync")
        engine_cache.sync_history(domains=[DOMAIN])
        print_live_table(db)

        # -------------------------------------------------------------
        # Step 3: snapshot sync
        # -------------------------------------------------------------
        print("\n>>> STEP 2: Snapshot Sync")
        engine_cache.sync_snapshot(
            domain=DOMAIN,
            root_node_id=ROOT_NODE_ID,
        )
        print_live_table(db)

        # -------------------------------------------------------------
        # Step 4: clear node cache
        # -------------------------------------------------------------
        print("\n>>> STEP 3: Clear Node Cache")
        engine_cache.clear_node_cache(
            domain=DOMAIN,
            root_node_id=ROOT_NODE_ID,
        )
        print_live_table(db)

    print("\n=== LOCAL CACHE MANUAL TEST END ===")


if __name__ == "__main__":
    main()