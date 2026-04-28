from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Optional

from OPE_DB_API.models import SessionMetadata


def _domain_session_id(domain: str) -> int:
    """
    Deterministically derive a synthetic session_id per domain.

    This avoids introducing a new metadata table.
    """
    # Stable, deterministic, non-zero.
    return abs(hash(f"LOCAL_CACHE::{domain}"))


# ---------------------------------------------------------
# Cursor read
# ---------------------------------------------------------

def get_last_history_id(db: Session, domain: str) -> Optional[int]:
    """
    Return the last synced history_id for a domain.
    """
    session_id = _domain_session_id(domain)
    meta = db.get(SessionMetadata, session_id)
    if meta is None:
        return None
    return meta.last_history_id


# ---------------------------------------------------------
# Cursor write
# ---------------------------------------------------------

def set_last_history_id(db: Session, domain: str, history_id: int) -> None:
    """
    Persist last synced history_id for a domain.

    This MUST be called only after successful replay commit.
    """
    session_id = _domain_session_id(domain)

    meta = db.get(SessionMetadata, session_id)
    if meta is None:
        meta = SessionMetadata(
            session_id=session_id,
            username="LOCAL_CACHE",
            hostname=domain,
            active=False,
        )
        db.add(meta)

    meta.last_history_id = history_id
    meta.last_synced_at = func.now()
    db.add(meta)