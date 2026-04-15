"""
Domain-specific table definitions.

Each domain defines:
- live data table
- overlay (session draft) table
- history (audit) table
"""

from .desi import (
    DesiData,
    DesiDataOverlay,
    DesiDataHistory,
)

from .cata import (
    CataData,
    CataDataOverlay,
    CataDataHistory,
)

from .dict import (
    DictData,
    DictDataOverlay,
    DictDataHistory,
)

from .engg import (
    EnggData,
    EnggDataOverlay,
    EnggDataHistory,
)

from .sche import (
    ScheData,
    ScheDataOverlay,
    ScheDataHistory,
)

from .sket import (
    SketData,
    SketDataOverlay,
    SketDataHistory,
)

from .admn import (
    AdmnData,
    AdmnDataHistory,
    AdmnDataOverlay,
)

__all__ = [
    "DesiData", "DesiDataOverlay", "DesiDataHistory",
    "CataData", "CataDataOverlay", "CataDataHistory",
    "DictData", "DictDataOverlay", "DictDataHistory",
    "EnggData", "EnggDataOverlay", "EnggDataHistory",
    "ScheData", "ScheDataOverlay", "ScheDataHistory",
    "SketData", "SketDataOverlay", "SketDataHistory",
    "AdmnData", "AdmnDataOverlay", "AdmnDataHistory",
]