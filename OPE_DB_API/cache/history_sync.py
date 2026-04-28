from typing import List, Dict, Any
from sqlalchemy.orm import Session

from OPE_DB_API.registry import HISTORY_TABLE_REGISTRY
from OPE_DB_API.cache.metadata import get_last_history_id
from OPE_DB_API.cache.metadata import set_last_history_id
from OPE_DB_API.cache.replayer import replay_domain_history

# HTTP client placeholder (replace with httpx or requests later)
from OPE_DB_API.cache.transport import fetch_history_batch


# ---------------------------------------------------------
# Public entry point (called by CacheEngine)
# ---------------------------------------------------------
def sync_domain_history(
    *,
    db: Session,
    code: str,
    domain: str,
    session_id: int,
) -> None:
    """
    Incrementally sync committed history for a single domain.

    Flow:
    1. Read cursor
    2. Fetch history from server
    3. Store locally
    4. Replay into domain_data
    5. Advance cursor (inside replayer)
    """
    last_history_id = get_last_history_id(db, domain)

    history_rows = fetch_history_batch(
        code=code,
        domain=domain,
        session_id=session_id,
        after_history_id=last_history_id,
    )

    if not history_rows:
        return

    from OPE_DB_API.registry import HISTORY_TABLE_REGISTRY
    model = HISTORY_TABLE_REGISTRY[domain]

    for row in history_rows:
        db.add(model(**row))

    db.commit()

    replay_domain_history(db=db, domain=domain)

    
# ---------------------------------------------------------
# Server pull
# ---------------------------------------------------------

def fetch_history_from_server(
    domain: str,
    after_history_id: int | None,
) -> List[Dict[str, Any]]:
    """
    Pull committed history rows from server.

    Returned rows MUST be:
    - Ordered by history_id ASC
    - Complete (no filtering on operation_type)
    """
    return fetch_history_batch(
        domain=domain,
        after_history_id=after_history_id,
    )


# ---------------------------------------------------------
# Local persistence
# ---------------------------------------------------------

def store_history_locally(
    db: Session,
    domain: str,
    rows: List[Dict[str, Any]],
) -> None:
    """
    Persist history rows into local <domain>_data_history table.
    """
    model = HISTORY_TABLE_REGISTRY[domain]

    for row in rows:
        db.add(model(**row))

    db.commit()
