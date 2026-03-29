from datetime import datetime

from pydantic import BaseModel

from app.core.enums import Role


class UserResponse(BaseModel):
    id: int
    name: str
    role: Role
    created_at: datetime

    model_config = {"from_attributes": True}
