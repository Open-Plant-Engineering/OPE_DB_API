from sqlalchemy.orm import Session

from OPE_DB_API.crud.work.push import push_work
from OPE_DB_API.crud.session import validate_session_active
from OPE_DB_API.errors import SessionNotActiveError


def push_work_bulk(
    db: Session,
    *,
    domain: str,
    session_id: int,
    items,
):
    """
    Bulk stage attribute changes into overlay.

    Partial success is allowed:
    - successful items are staged
    - failures are reported
    """

    # Validate session once
    validate_session_active(db, session_id=session_id)

    success = []
    failure = []

    for item in items:
        try:
            row = push_work(
                db=db,
                domain=domain,
                session_id=session_id,
                payload=item,
            )
            success.append(row.data_id)

        except SessionNotActiveError:
            # Session error should abort whole request
            raise

        except Exception as exc:
            failure.append({
                "data_id": item.data_id,
                "reason": exc.__class__.__name__,
            })

    return success, failure