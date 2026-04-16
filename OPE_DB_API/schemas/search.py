from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Atomic filter condition
# ---------------------------------------------------------

class SearchCondition(BaseModel):
    field: str
    op: Literal[
        "=", "!=", ">", "<", ">=", "<=",
        "in",
        "contains",
        "json_contains",
        "json_key_exists"
    ]
    value: Any


# ---------------------------------------------------------
# Logical groups (recursive)
# ---------------------------------------------------------

class SearchAnd(BaseModel):
    and_: List["SearchNode"] = Field(..., alias="and")


class SearchOr(BaseModel):
    or_: List["SearchNode"] = Field(..., alias="or")


class SearchNot(BaseModel):
    not_: "SearchNode" = Field(..., alias="not")


SearchNode = Union[
    SearchCondition,
    SearchAnd,
    SearchOr,
    SearchNot,
]

# ---------------------------------------------------------
# Final request
# ---------------------------------------------------------

class SearchRequest(BaseModel):
    mode: Literal["live", "working"] = "live"
    filter: Optional[SearchNode] = None
    limit: int = 50
    offset: int = 0


SearchAnd.model_rebuild()
SearchOr.model_rebuild()
SearchNot.model_rebuild()