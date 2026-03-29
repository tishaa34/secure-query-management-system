from sqlalchemy.orm import Session

from app.core.exceptions import AuthorizationError, NotFoundError
from app.modules.audit.models import AuditLog
from app.modules.audit.repository import AuditRepository
from app.modules.queries.repository import QueryRepository
from app.modules.queries.service import QueryService
from app.modules.users.models import User


class AuditService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.audit_repository = AuditRepository(db)
        self.query_repository = QueryRepository(db)
        self.query_service = QueryService(db)

    def get_query_audit(self, query_id: int, actor: User) -> list[AuditLog]:
        query = self.query_repository.get_by_id(query_id)
        if query is None:
            raise NotFoundError(f"Query {query_id} was not found.")
        if not self.query_service.can_view_query(actor, query):
            raise AuthorizationError("You do not have access to this query audit trail.")
        return self.audit_repository.list_for_query(query_id)
