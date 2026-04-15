"""
Table registry for ope_db_api.

Maps domain codes to SQLAlchemy ORM models.
Acts as a security layer to prevent arbitrary table access.
"""

from OPE_DB_API.domains import (
    DesiData,
    DesiDataOverlay,
    DesiDataHistory,

    CataData,
    CataDataOverlay,
    CataDataHistory,

    DictData,
    DictDataOverlay,
    DictDataHistory,

    EnggData,
    EnggDataOverlay,
    EnggDataHistory,

    ScheData,
    ScheDataOverlay,
    ScheDataHistory,

    SketData,
    SketDataOverlay,
    SketDataHistory,

    AdmnData,
    AdmnDataOverlay,
    AdmnDataHistory,
)


# ---------------------------------------------------------
# Live (authoritative) data tables
# ---------------------------------------------------------

LIVE_TABLE_REGISTRY = {
    "DESI": DesiData,
    "CATA": CataData,
    "DICT": DictData,
    "ENGG": EnggData,
    "SCHE": ScheData,
    "SKET": SketData,
    "ADMN": AdmnData,
}


# ---------------------------------------------------------
# Session overlay (draft) tables
# ---------------------------------------------------------

OVERLAY_TABLE_REGISTRY = {
    "DESI": DesiDataOverlay,
    "CATA": CataDataOverlay,
    "DICT": DictDataOverlay,
    "ENGG": EnggDataOverlay,
    "SCHE": ScheDataOverlay,
    "SKET": SketDataOverlay,
    "ADMN": AdmnDataOverlay,
}


# ---------------------------------------------------------
# History (immutable audit) tables
# ---------------------------------------------------------

HISTORY_TABLE_REGISTRY = {
    "DESI": DesiDataHistory,
    "CATA": CataDataHistory,
    "DICT": DictDataHistory,
    "ENGG": EnggDataHistory,
    "SCHE": ScheDataHistory,
    "SKET": SketDataHistory,
    "ADMN": AdmnDataHistory,
}