from sqlalchemy.orm import Session

from OPE_DB_API.registry import (
    LIVE_TABLE_REGISTRY,
    HISTORY_TABLE_REGISTRY,
)

from OPE_DB_API.cache.metadata import set_last_history_id


# ---------------------------------------------------------
# Public entry point
# ---------------------------------------------------------

def replay_domain_history(db: Session, domain: str) -> None:
    """
    Replay all locally staged history rows for a domain
    into local <domain>_data.

    Guarantees:
    - Row-by-row deterministic replay
    - Atomic commit
    - Safe cursor advancement
    """
    history_model = HISTORY_TABLE_REGISTRY[domain]
    live_model = LIVE_TABLE_REGISTRY[domain]

    # Fetch history in strict order
    history_rows = (
        db.query(history_model)
        .order_by(history_model.history_id.asc())
        .all()
    )

    if not history_rows:
        return

    max_history_id = None

    for row in history_rows:
        _apply_history_row(
            db=db,
            live_model=live_model,
            history_row=row,
        )
        max_history_id = row.history_id

    # Commit all live data mutations first
    db.commit()

    # Advance cursor ONLY after successful replay
    set_last_history_id(db, domain, max_history_id)
    db.commit()

    # Clear local history bucket
    for row in history_rows:
        db.delete(row)

    db.commit()


# ---------------------------------------------------------
# Row-level replay logic
# ---------------------------------------------------------

def _apply_history_row(db: Session, live_model, history_row) -> None:
    """
    Apply a single history record to local live data.
    """
    data_id = history_row.data_id
    op = history_row.operation_type

    live_row = db.get(live_model, data_id)

    # ---------------------------------------------
    # CREATE
    # ---------------------------------------------
    if op == 1:
        if live_row is not None:
            return  # ignore duplicate create

        db.add(
            live_model(
                data_id=data_id,
                node_id=history_row.new_value.get("node_id")
                if history_row.new_value else None,
                attribute_id=history_row.new_value.get("attribute_id")
                if history_row.new_value else None,
                value=history_row.new_value,
            )
        )
        return

    # ---------------------------------------------
    # UPDATE
    # ---------------------------------------------
    if op == 2:
        if live_row is None:
            db.add(
                live_model(
                    data_id=data_id,
                    node_id=history_row.new_value.get("node_id")
                    if history_row.new_value else None,
                    attribute_id=history_row.new_value.get("attribute_id")
                    if history_row.new_value else None,
                    value=history_row.new_value,
                )
            )
        else:
            live_row.value = history_row.new_value
            db.add(live_row)
        return

    # ---------------------------------------------
    # DELETE
    # ---------------------------------------------
    if op == 3:
        if live_row is not None:
            db.delete(live_row)
        return
