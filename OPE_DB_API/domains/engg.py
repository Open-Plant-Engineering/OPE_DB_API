from sqlalchemy import UniqueConstraint

from OPE_DB_API.models import (
    DbDataBase,
    DbDataOverlayBase,
    DbDataHistoryBase,
)


class EnggData(DbDataBase):
    __tablename__ = "engg_data"
    __table_args__ = (
        UniqueConstraint("node_id", "attribute_id", name="engg_data_uq_node_attribute"),
    )

class EnggDataOverlay(DbDataOverlayBase):
    __tablename__ = "engg_data_overlay"


class EnggDataHistory(DbDataHistoryBase):
    __tablename__ = "engg_data_history"