from datetime import datetime

from pydantic import BaseModel

from app.core.enums import AuditAction
from app.modules.users.schemas import UserResponse


class AuditLogResponse(BaseModel):
    id: int
    query_id: int
    action: AuditAction
    performed_by: UserResponse
    timestamp: datetime

    model_config = {"from_attributes": True}
