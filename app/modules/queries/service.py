from sqlalchemy.orm import Session

from app.core.enums import AuditAction, QueryPriority, QueryStatus, Role
from app.core.exceptions import AuthorizationError, NotFoundError, ValidationError
from app.modules.audit.repository import AuditRepository
from app.modules.queries.models import Query
from app.modules.queries.repository import QueryRepository
from app.modules.queries.schemas import AssignQueryRequest, QueryCreateRequest, QueryStatusUpdateRequest
from app.modules.queries.workflow import ensure_valid_transition
from app.modules.users.models import User
from app.modules.users.service import UserService


class QueryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.query_repository = QueryRepository(db)
        self.audit_repository = AuditRepository(db)
        self.user_service = UserService(db)

    def create_query(self, payload: QueryCreateRequest, actor: User) -> Query:
        query = Query(
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            status=QueryStatus.NEW,
            created_by_id=actor.id,
        )
        created_query = self.query_repository.create(query)
        self.audit_repository.create(
            query_id=created_query.id,
            action=AuditAction.CREATED,
            performed_by_id=actor.id,
        )
        self.db.commit()
        return self.query_repository.get_by_id(created_query.id) or created_query

    def list_queries(
        self,
        actor: User,
        status: QueryStatus | None = None,
        priority: QueryPriority | None = None,
    ) -> list[Query]:
        return self.query_repository.list_for_actor(actor, status=status, priority=priority)

    def assign_query(self, query_id: int, payload: AssignQueryRequest, actor: User) -> Query:
        query = self._get_query_or_fail(query_id)
        assignee = self.user_service.get_user_or_fail(payload.assigned_to_id)

        if assignee.role != Role.RESOLVER:
            raise ValidationError("Queries can only be assigned to users with the RESOLVER role.")
        if query.status == QueryStatus.RESOLVED:
            raise ValidationError("Resolved queries cannot be reassigned.")

        query.assigned_to_id = assignee.id

        # First assignment is the workflow entry point into active handling.
        if query.status == QueryStatus.NEW:
            query.status = QueryStatus.ASSIGNED

        self.audit_repository.create(
            query_id=query.id,
            action=AuditAction.ASSIGNED,
            performed_by_id=actor.id,
        )
        self.db.commit()
        return self.query_repository.get_by_id(query.id) or query

    def update_status(self, query_id: int, payload: QueryStatusUpdateRequest, actor: User) -> Query:
        query = self._get_query_or_fail(query_id)
        self._authorize_status_update(actor, query)

        if payload.status == QueryStatus.ASSIGNED and query.assigned_to_id is None:
            raise ValidationError("A query must be assigned before its status can move to ASSIGNED.")

        ensure_valid_transition(query.status, payload.status)
        query.status = payload.status

        self.audit_repository.create(
            query_id=query.id,
            action=AuditAction.STATUS_CHANGED,
            performed_by_id=actor.id,
        )
        self.db.commit()
        return self.query_repository.get_by_id(query.id) or query

    def can_view_query(self, actor: User, query: Query) -> bool:
        if actor.role == Role.ADMIN:
            return True
        if actor.role == Role.USER:
            return query.created_by_id == actor.id
        if actor.role == Role.RESOLVER:
            return query.assigned_to_id == actor.id
        return False

    def _get_query_or_fail(self, query_id: int) -> Query:
        query = self.query_repository.get_by_id(query_id)
        if query is None:
            raise NotFoundError(f"Query {query_id} was not found.")
        return query

    def _authorize_status_update(self, actor: User, query: Query) -> None:
        if actor.role == Role.ADMIN:
            return
        if actor.role == Role.RESOLVER and query.assigned_to_id == actor.id:
            return
        raise AuthorizationError("Only admins or the assigned resolver can update query status.")
