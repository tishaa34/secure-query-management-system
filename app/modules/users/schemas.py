from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums import Role


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    role: Role


class UserResponse(BaseModel):
    id: int
    name: str
    role: Role
    created_at: datetime

    model_config = {"from_attributes": True}
