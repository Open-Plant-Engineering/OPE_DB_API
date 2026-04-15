from OPE_DB_API.models import (
    DbDataBase,
    DbDataHistoryBase,
    DbDataOverlayBase,
)


class AdmnData(DbDataBase):
    __tablename__ = "admn_data"


class AdmnDataOverlay(DbDataOverlayBase):
    __tablename__ = "admn_data_overlay"


class AdmnDataHistory(DbDataHistoryBase):
    __tablename__ = "admn_data_history"