from sqlalchemy.orm import Session
from OPE_DB_API.registry import (
    LIVE_TABLE_REGISTRY,
    OVERLAY_TABLE_REGISTRY,
)

def read_current_work(
    db: Session,
    *,
    domain: str,
    session_id: int,
):
    """
    Return merged view of live data plus session overlay.
    Overlay shadows live data by data_id.
    """

    Live = LIVE_TABLE_REGISTRY[domain]
    Overlay = OVERLAY_TABLE_REGISTRY[domain]

    # Fetch overlay rows for session
    overlay_rows = db.query(Overlay).filter(
        Overlay.session_id == session_id
    ).all()

    overlay_map = {row.data_id: row for row in overlay_rows}

    # Fetch all live rows
    live_rows = db.query(Live).all()

    result = []

    for live in live_rows:
        overlay = overlay_map.pop(live.data_id, None)

        if overlay:
            if overlay.operation_type == 3:  # DELETE
                continue
            result.append(overlay)
        else:
            result.append(live)

    # Remaining overlay rows are CREATEs
    for overlay in overlay_map.values():
        if overlay.operation_type == 1:
            result.append(overlay)

    return result