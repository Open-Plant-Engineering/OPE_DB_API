from pydantic import BaseModel
from typing import Optional, List, Any

class WorkPushRequest(BaseModel):
    data_id: Optional[int]     # None = CREATE
    node_id: int
    attribute_id: int
    operation_type: int        # 1 = CREATE, 2 = UPDATE, 3 = DELETE
    value: Optional[Any]      # None only allowed for DELETE

class BulkWorkPushRequest(BaseModel):
    items: List[WorkPushRequest]