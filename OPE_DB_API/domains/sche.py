from OPE_DB_API.models import (
    DbDataBase,
    DbDataOverlayBase,
    DbDataHistoryBase,
)


class ScheData(DbDataBase):
    __tablename__ = "sche_data"


class ScheDataOverlay(DbDataOverlayBase):
    __tablename__ = "sche_data_overlay"


class ScheDataHistory(DbDataHistoryBase):
    __tablename__ = "sche_data_history"