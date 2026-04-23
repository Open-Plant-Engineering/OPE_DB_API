from sqlalchemy.orm import Session

from OPE_DB_API.registry import (
    LIVE_TABLE_REGISTRY,
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

def commit_session(
    db: Session,
    *,
    domain: str,
    session_id: int,
):
    """
    Commit all staged overlay changes for a session.
    """

    validate_session_active(db, session_id=session_id)

    Live = LIVE_TABLE_REGISTRY[domain]
    Overlay = OVERLAY_TABLE_REGISTRY[domain]

    overlay_rows = db.query(Overlay).filter(
        Overlay.session_id == session_id
    ).all()

    for o in [x for x in overlay_rows if x.operation_type == 1]: # CREATE 
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
    
    db.flush()
    
    for o in [x for x in overlay_rows if x.operation_type == 2]: # UPDATE 
        live = get_live_row(db, domain, o.data_id)
        # Guard: UPDATE / DELETE must have existing live row
        if live is None:
            raise ValueError(
                f"Cannot apply operation {o.operation_type} "
                f"because live row does not exist for data_id={o.data_id}"
            )
        
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

    db.flush()

    for o in [x for x in overlay_rows if x.operation_type == 3]: # DELETE 
        live = get_live_row(db, domain, o.data_id)
        # Guard: UPDATE / DELETE must have existing live row
        if live is None:
            raise ValueError(
                f"Cannot apply operation {o.operation_type} "
                f"because live row does not exist for data_id={o.data_id}"
            )
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

    db.flush()
    
    # Clear overlay
    db.query(Overlay).filter(
        Overlay.session_id == session_id
    ).delete()

    close_session(db, session_id=session_id)
