from sqlalchemy.orm import Session
from typing import Iterable, Optional

from OPE_DB_API.registry import LIVE_TABLE_REGISTRY
from OPE_DB_API.cache.history_sync import sync_domain_history
from OPE_DB_API.cache.snapshot_sync import sync_domain_snapshot
from OPE_DB_API.cache.cleanup import clear_domain_node_cache


class CacheEngine:
    """
    High-level coordinator for local cache synchronization.
    """

    def __init__(self, *, db: Session, code: str, session_id: int):
        self.db = db
        self.code = code
        self.session_id = session_id

    def _get_domains(self, domains: Optional[Iterable[str]] = None) -> Iterable[str]:
        return domains or LIVE_TABLE_REGISTRY.keys()

    # ---------------------------------------------------------
    # Incremental history sync
    # ---------------------------------------------------------

    def sync_history(self, domains: Optional[Iterable[str]] = None) -> None:
        for domain in self._get_domains(domains):
            sync_domain_history(
                db=self.db,
                code=self.code,
                domain=domain,
                session_id=self.session_id,
            )

    # ---------------------------------------------------------
    # Snapshot / hierarchy sync
    # ---------------------------------------------------------

    def sync_snapshot(self, *, domain: str, root_node_id: int) -> None:
        sync_domain_snapshot(
            db=self.db,
            code=self.code,
            domain=domain,
            session_id=self.session_id,
            root_node_id=root_node_id,
        )

    # ---------------------------------------------------------
    # Local cache cleanup
    # ---------------------------------------------------------

    def clear_node_cache(self, *, domain: str, root_node_id: int) -> None:
        clear_domain_node_cache(
            db=self.db,
            domain=domain,
            root_node_id=root_node_id,
        )
