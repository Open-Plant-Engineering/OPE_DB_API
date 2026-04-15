from OPE_DB_API.models import (
    DbDataBase,
    DbDataOverlayBase,
    DbDataHistoryBase,
)


class DesiData(DbDataBase):
    """
    Live, authoritative data for DESI domain.
    """
    __tablename__ = "desi_data"


class DesiDataOverlay(DbDataOverlayBase):
    """
    Session overlay data for DESI domain.
    """
    __tablename__ = "desi_data_overlay"


class DesiDataHistory(DbDataHistoryBase):
    """
    Immutable history log for DESI domain.
    """
    __tablename__ = "desi_data_history"