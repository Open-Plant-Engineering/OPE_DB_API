from OPE_DB_API.models import (
    DbDataBase,
    DbDataOverlayBase,
    DbDataHistoryBase,
)


class DictData(DbDataBase):
    __tablename__ = "dict_data"


class DictDataOverlay(DbDataOverlayBase):
    __tablename__ = "dict_data_overlay"


class DictDataHistory(DbDataHistoryBase):
    __tablename__ = "dict_data_history"
