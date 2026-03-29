from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_session
from app.core.security import get_current_user
from app.modules.audit.schemas import AuditLogResponse
from app.modules.audit.service import AuditService
from app.modules.users.models import User

router = APIRouter(prefix="/queries", tags=["audit"])


@router.get("/{query_id}/audit", response_model=list[AuditLogResponse])
def get_query_audit(
    query_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[AuditLogResponse]:
    return AuditService(db).get_query_audit(query_id, current_user)
