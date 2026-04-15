from OPE_DB_API.models import (
    DbDataBase,
    DbDataOverlayBase,
    DbDataHistoryBase,
)


class CataData(DbDataBase):
    __tablename__ = "cata_data"


class CataDataOverlay(DbDataOverlayBase):
    __tablename__ = "cata_data_overlay"


class CataDataHistory(DbDataHistoryBase):
    __tablename__ = "cata_data_history"