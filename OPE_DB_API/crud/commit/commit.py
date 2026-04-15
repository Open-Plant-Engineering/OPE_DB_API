from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from OPE_DB_API.registry import (
    LIVE_TABLE_REGISTRY,
    OVERLAY_TABLE_REGISTRY,
    HISTORY_TABLE_REGISTRY,
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

    This operation is atomic:
    - applies overlay changes to live tables
    - writes history
    - deletes overlay rows
    - closes session

    Raises on any error; DB transaction ensures rollback.
    """

    # -----------------------------------------------------
    # 1. Validate session
    # -----------------------------------------------------

    validate_session_active(db, session_id=session_id)

    overlay_model = OVERLAY_TABLE_REGISTRY[domain]
    live_model = LIVE_TABLE_REGISTRY[domain]
    history_model = HISTORY_TABLE_REGISTRY[domain]

    try:
        # -------------------------------------------------
        # 2. Load overlay rows for this session
        # -------------------------------------------------

        overlay_rows = (
            db.query(overlay_model)
            .filter(overlay_model.session_id == session_id)
            .all()
        )

        # -------------------------------------------------
        # 3. Apply each overlay row
        # -------------------------------------------------

        for overlay in overlay_rows:
            data_id = overlay.overlay_id
            new_value = overlay.value

            live_row = get_live_row(db, domain, data_id)

            # -----------------------------
            # CREATE
            # -----------------------------
            if live_row is None and new_value is not None:
                insert_live_row(
                    db,
                    domain,
                    {
                        "data_id": data_id,
                        "node_id": overlay.node_id,
                        "attribute_id": overlay.attribute_id,
                        "value": new_value,
                    },
                )

                write_history(
                    db,
                    domain,
                    {
                        "history_id": overlay.overlay_id,
                        "data_id": data_id,
                        "session_id": session_id,
                        "operation_type": 1,  # CREATE
                        "old_value": None,
                        "new_value": new_value,
                    },
                )

            # -----------------------------
            # UPDATE
            # -----------------------------
            elif live_row is not None and new_value is not None:
                old_value = live_row.value

                update_live_row(db, live_row, new_value)

                write_history(
                    db,
                    domain,
                    {
                        "history_id": overlay.overlay_id,
                        "data_id": data_id,
                        "session_id": session_id,
                        "operation_type": 2,  # UPDATE
                        "old_value": old_value,
                        "new_value": new_value,
                    },
                )

            # -----------------------------
            # DELETE
            # -----------------------------
            elif live_row is not None and new_value is None:
                old_value = live_row.value

                delete_live_row(db, live_row)

                write_history(
                    db,
                    domain,
                    {
                        "history_id": overlay.overlay_id,
                        "data_id": data_id,
                        "session_id": session_id,
                        "operation_type": 3,  # DELETE
                        "old_value": old_value,
                        "new_value": None,
                    },
                )

            # -----------------------------
            # Invalid state
            # -----------------------------
            else:
                raise RuntimeError(
                    f"Invalid overlay state for data_id={data_id}"
                )

            # -------------------------------------------------
            # 4. Remove overlay row after processing
            # -------------------------------------------------

            db.delete(overlay)

        # -----------------------------------------------------
        # 5. Close session
        # -----------------------------------------------------

        close_session(db, session_id=session_id)

        # -----------------------------------------------------
        # 6. Commit transaction
        # -----------------------------------------------------

        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise