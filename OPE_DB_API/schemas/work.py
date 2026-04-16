from pydantic import BaseModel
from typing import Optional, Dict, List

class WorkPushRequest(BaseModel):
    data_id: Optional[int]     # None = CREATE
    node_id: int
    attribute_id: int
    operation_type: int        # 1 = CREATE, 2 = UPDATE, 3 = DELETE
    value: Optional[Dict]      # None only allowed for DELETE

class WorkPushRequest(BaseModel):
    items: List[WorkPushRequest]