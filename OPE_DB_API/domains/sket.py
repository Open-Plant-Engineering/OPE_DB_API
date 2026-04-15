from OPE_DB_API.models import (
    DbDataBase,
    DbDataOverlayBase,
    DbDataHistoryBase,
)


class SketData(DbDataBase):
    __tablename__ = "sket_data"


class SketDataOverlay(DbDataOverlayBase):
    __tablename__ = "sket_data_overlay"


class SketDataHistory(DbDataHistoryBase):
    __tablename__ = "sket_data_history"