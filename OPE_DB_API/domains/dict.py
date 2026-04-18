from sqlalchemy import UniqueConstraint

from OPE_DB_API.models import (
    DbDataBase,
    DbDataOverlayBase,
    DbDataHistoryBase,
)


class DictData(DbDataBase):
    __tablename__ = "dict_data"
    __table_args__ = (
        UniqueConstraint("node_id", "attribute_id", name="dict_data_uq_node_attribute"),
    )

class DictDataOverlay(DbDataOverlayBase):
    __tablename__ = "dict_data_overlay"


class DictDataHistory(DbDataHistoryBase):
    __tablename__ = "dict_data_history"
