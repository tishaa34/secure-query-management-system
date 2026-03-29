from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import AuditAction
from app.modules.audit.models import AuditLog


class AuditRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, query_id: int, action: AuditAction, performed_by_id: int) -> AuditLog:
        entry = AuditLog(query_id=query_id, action=action, performed_by_id=performed_by_id)
        self.db.add(entry)
        self.db.flush()
        self.db.refresh(entry)
        return entry

    def list_for_query(self, query_id: int) -> list[AuditLog]:
        statement = (
            select(AuditLog)
            .options(joinedload(AuditLog.performed_by))
            .where(AuditLog.query_id == query_id)
            .order_by(AuditLog.timestamp.asc())
        )
        return list(self.db.scalars(statement).all())
