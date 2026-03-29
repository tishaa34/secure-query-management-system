from pydantic import BaseModel, Field

from app.core.enums import Role


class LoginRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: Role
