from sqlalchemy.orm import Session
from OPE_DB_API.registry import LIVE_TABLE_REGISTRY


def insert_live_row(db: Session, domain: str, payload: dict):
    model = LIVE_TABLE_REGISTRY[domain]
    row = model(**payload)
    db.add(row)
    return row


def update_live_row(db: Session, row, new_value):
    row.value = new_value
    db.add(row)
    return row


def delete_live_row(db: Session, row):
    db.delete(row)