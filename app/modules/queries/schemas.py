from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums import QueryPriority, QueryStatus
from app.modules.users.schemas import UserResponse


class QueryCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5)
    priority: QueryPriority | None = None


class AssignQueryRequest(BaseModel):
    assigned_to_id: int = Field(gt=0)


class QueryStatusUpdateRequest(BaseModel):
    status: QueryStatus


class QueryResponse(BaseModel):
    id: int
    title: str
    description: str
    status: QueryStatus
    priority: QueryPriority | None
    created_by: UserResponse
    assigned_to: UserResponse | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
