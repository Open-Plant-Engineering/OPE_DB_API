from sqlalchemy.orm import Session

from OPE_DB_API.registry import (
    OVERLAY_TABLE_REGISTRY,
)
from OPE_DB_API.crud.session import (
    validate_session_active,
    close_session,
)
from OPE_DB_API.crud.live.read import get_live_row
from OPE_DB_API.crud.live.write import (
    insert_live_row,
    update_live_row,
    delete_live_row,
)
from OPE_DB_API.crud.history.write import write_history
from OPE_DB_API.crud.sync.snapshot import fetch_snapshot_subtree

def commit_session(
    db: Session,
    *,
    domain: str,
    session_id: int,
    owner_attribute_id: int | None = None
):
    """
    Commit all staged overlay changes for a session.
    """

    validate_session_active(db, session_id=session_id)

    Overlay = OVERLAY_TABLE_REGISTRY[domain]

    overlay_rows = db.query(Overlay).filter(
        Overlay.session_id == session_id
    ).all()

    for o in overlay_rows:
        live = get_live_row(db, domain, o.data_id)

        # Guard: UPDATE / DELETE must have existing live row
        if o.operation_type in (2, 3) and live is None:
            print(
                f"Cannot apply operation {o.operation_type} "
                f"because live row does not exist for data_id={o.data_id}"
            )
            continue

        if o.operation_type == 1:  # CREATE
            insert_live_row(
                db,
                domain,
                {
                    "data_id": o.data_id,
                    "node_id": o.node_id,
                    "attribute_id": o.attribute_id,
                    "value": o.value,
                },
            )
            write_history(
                db,
                domain,
                {
                    "data_id": o.data_id,
                    "session_id": session_id,
                    "operation_type": 1,
                    "old_value": None,
                    "new_value": o.value,
                },
            )

        elif o.operation_type == 2:  # UPDATE
            old_value = live.value
            update_live_row(db, live, o.value)
            write_history(
                db,
                domain,
                {
                    "data_id": o.data_id,
                    "session_id": session_id,
                    "operation_type": 2,
                    "old_value": old_value,
                    "new_value": o.value,
                },
            )
            
        elif o.operation_type == 3:  # DELETE
            if owner_attribute_id is not None:
                    root_node_id = live.node_id

                    subtree_rows = fetch_snapshot_subtree(
                        db=db,
                        domain=domain,
                        root_node_id=root_node_id,
                        owner_attribute_id=owner_attribute_id,
                    )

                    for row in subtree_rows:
                        live_row = get_live_row(db, domain, row.data_id)
                        if live_row is None:
                            continue
                        
                        old_value = live_row.value
                        delete_live_row(db, live_row)

                        write_history(
                            db,
                            domain,
                            {
                                "data_id": live_row.data_id,
                                "session_id": session_id,
                                "operation_type": 3,
                                "old_value": old_value,
                                "new_value": None,
                            },
                        )

            # ✅ CASE 2: Single-row delete (current behavior)
            else:
                old_value = live.value
                delete_live_row(db, live)

                write_history(
                    db,
                    domain,
                    {
                        "data_id": o.data_id,
                        "session_id": session_id,
                        "operation_type": 3,
                        "old_value": old_value,
                        "new_value": None,
                    },
                )

    
    # Clear overlay
    db.query(Overlay).filter(
        Overlay.session_id == session_id
    ).delete()

    close_session(db, session_id=session_id)
