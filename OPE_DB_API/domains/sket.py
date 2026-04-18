from sqlalchemy import UniqueConstraint

from OPE_DB_API.models import (
    DbDataBase,
    DbDataOverlayBase,
    DbDataHistoryBase,
)


class SketData(DbDataBase):
    __tablename__ = "sket_data"
    __table_args__ = (
        UniqueConstraint("node_id", "attribute_id", name="sket_data_uq_node_attribute"),
    )

class SketDataOverlay(DbDataOverlayBase):
    __tablename__ = "sket_data_overlay"


class SketDataHistory(DbDataHistoryBase):
    __tablename__ = "sket_data_history"