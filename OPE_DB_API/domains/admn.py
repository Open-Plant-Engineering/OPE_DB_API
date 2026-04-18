from sqlalchemy import UniqueConstraint

from OPE_DB_API.models import (
    DbDataBase,
    DbDataHistoryBase,
    DbDataOverlayBase,
)


class AdmnData(DbDataBase):
    __tablename__ = "admn_data"
    __table_args__ = (
        UniqueConstraint("node_id", "attribute_id", name="admn_data_uq_node_attribute"),
    )

class AdmnDataOverlay(DbDataOverlayBase):
    __tablename__ = "admn_data_overlay"


class AdmnDataHistory(DbDataHistoryBase):
    __tablename__ = "admn_data_history"