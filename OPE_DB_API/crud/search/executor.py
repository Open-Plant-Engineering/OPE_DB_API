from sqlalchemy.orm import Session

from OPE_DB_API.registry import (
    LIVE_TABLE_REGISTRY,
    OVERLAY_TABLE_REGISTRY,
)
from OPE_DB_API.crud.session import get_active_session
from OPE_DB_API.crud.search.compiler import compile_search
from OPE_DB_API.crud.search.python_eval import eval_search_node

def execute_live_search(
    db: Session,
    *,
    domain: str,
    session_id: int,
    search,
):
    """
    Execute search directly on live table.
    """

    Model = LIVE_TABLE_REGISTRY[domain]

    query = db.query(Model)

    # Apply filters
    if search.filter:
        condition = compile_search(Model, domain, search.filter)
        query = query.filter(condition)

    total = query.count()

    # Pagination
    query = query.offset(search.offset).limit(search.limit)

    return {
        "total": total,
        "items": query.all(),
    }


def execute_working_search(
    db: Session,
    *,
    domain: str,
    session_id: int,
    search,
):
    """
    Execute search on merged Live ⊕ Overlay view.
    """

    Live = LIVE_TABLE_REGISTRY[domain]
    Overlay = OVERLAY_TABLE_REGISTRY[domain]

    # Fetch data
    live_rows = db.query(Live).all()
    overlay_rows = db.query(Overlay).filter(
        Overlay.session_id == session_id  # see note below
    ).all()

    overlay_map = {o.data_id: o for o in overlay_rows}

    # Merge
    merged = {}

    for live in live_rows:
        overlay = overlay_map.pop(live.data_id, None)

        if overlay:
            if overlay.operation_type == 3:
                continue  # DELETE
            merged[live.data_id] = overlay
        else:
            merged[live.data_id] = live

    # Remaining overlay rows are CREATEs
    for overlay in overlay_map.values():
        if overlay.operation_type == 1:
            merged[overlay.data_id] = overlay

    rows = list(merged.values())

    # Apply filtering manually (Python-side)
    if search.filter:
        rows = [r for r in rows if eval_search_node(r, search.filter)]

    total = len(rows)

    # Pagination
    rows = rows[search.offset : search.offset + search.limit]

    return {
        "total": total,
        "items": rows,
    }


def execute_search(
    db: Session,
    *,
    domain: str,
    session_id: int,
    search,
):
    if search.mode == "working":
        return execute_working_search(
            db,
            domain=domain,
            search=search,
        )
    return execute_live_search(
        db,
        domain=domain,
        search=search,
    )