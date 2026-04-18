from sqlalchemy import UniqueConstraint

from OPE_DB_API.models import (
    DbDataBase,
    DbDataOverlayBase,
    DbDataHistoryBase,
)


class CataData(DbDataBase):
    __tablename__ = "cata_data"
    __table_args__ = (
        UniqueConstraint("node_id", "attribute_id", name="cata_data_uq_node_attribute"),
    )


class CataDataOverlay(DbDataOverlayBase):
    __tablename__ = "cata_data_overlay"


class CataDataHistory(DbDataHistoryBase):
    __tablename__ = "cata_data_history"