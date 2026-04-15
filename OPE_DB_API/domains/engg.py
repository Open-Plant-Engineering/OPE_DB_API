from OPE_DB_API.models import (
    DbDataBase,
    DbDataOverlayBase,
    DbDataHistoryBase,
)


class EnggData(DbDataBase):
    __tablename__ = "engg_data"


class EnggDataOverlay(DbDataOverlayBase):
    __tablename__ = "engg_data_overlay"


class EnggDataHistory(DbDataHistoryBase):
    __tablename__ = "engg_data_history"