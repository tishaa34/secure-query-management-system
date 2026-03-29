from sqlalchemy import Select, select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import QueryPriority, QueryStatus, Role
from app.modules.queries.models import Query
from app.modules.users.models import User


class QueryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, query: Query) -> Query:
        self.db.add(query)
        self.db.flush()
        self.db.refresh(query)
        return query

    def get_by_id(self, query_id: int) -> Query | None:
        statement = (
            select(Query)
            .options(joinedload(Query.created_by), joinedload(Query.assigned_to))
            .where(Query.id == query_id)
        )
        return self.db.scalar(statement)

    def list_for_actor(
        self,
        actor: User,
        status: QueryStatus | None = None,
        priority: QueryPriority | None = None,
    ) -> list[Query]:
        statement: Select[tuple[Query]] = (
            select(Query)
            .options(joinedload(Query.created_by), joinedload(Query.assigned_to))
            .order_by(Query.created_at.desc())
        )

        if actor.role == Role.USER:
            statement = statement.where(Query.created_by_id == actor.id)
        elif actor.role == Role.RESOLVER:
            statement = statement.where(Query.assigned_to_id == actor.id)

        if status is not None:
            statement = statement.where(Query.status == status)
        if priority is not None:
            statement = statement.where(Query.priority == priority)

        return list(self.db.scalars(statement).all())
