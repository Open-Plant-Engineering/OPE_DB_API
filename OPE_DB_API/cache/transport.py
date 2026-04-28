import httpx
from typing import List, Dict, Any, Optional

from OPE_DB_API.config import get_config
from OPE_DB_API.config.loader import get_client_config

# ---------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------

def _get_base_url() -> str:
    """
    Resolve server base URL from config.
    """
    config = get_client_config()
    return config.get("server", {}).get("base_url", "http://localhost:8000")


def _build_url(
    code: str,
    domain: str,
    session_id: int,
    path: str,
) -> str:
    base_url = _get_base_url()
    return f"{base_url}/{code}/{domain}/{session_id}/sync{path}"


# ---------------------------------------------------------
# History transport
# ---------------------------------------------------------

def fetch_history_batch(
    *,
    code: str,
    domain: str,
    session_id: int,
    after_history_id: Optional[int],
    limit: int = 5000,
) -> List[Dict[str, Any]]:
    """
    Fetch a batch of committed history rows from server.
    """
    url = _build_url(
        code=code,
        domain=domain,
        session_id=session_id,
        path="/history",
    )

    params = {
        "after_history_id": after_history_id,
        "limit": limit,
    }

    with httpx.Client() as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------
# Snapshot transport
# ---------------------------------------------------------

def fetch_snapshot_subtree(
    *,
    code: str,
    domain: str,
    session_id: int,
    root_node_id: int,
) -> List[Dict[str, Any]]:
    """
    Fetch authoritative subtree snapshot from server.
    """
    url = _build_url(
        code=code,
        domain=domain,
        session_id=session_id,
        path="/snapshot",
    )

    params = {
        "root_node_id": root_node_id,
    }

    with httpx.Client() as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        return response.json()