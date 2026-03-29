from fastapi import APIRouter, Depends, Query as QueryParam
from sqlalchemy.orm import Session

from app.api.dependencies import get_session, require_roles
from app.core.enums import QueryPriority, QueryStatus, Role
from app.core.security import get_current_user
from app.modules.queries.schemas import (
    AssignQueryRequest,
    QueryCreateRequest,
    QueryResponse,
    QueryStatusUpdateRequest,
)
from app.modules.queries.service import QueryService
from app.modules.users.models import User

router = APIRouter(prefix="/queries", tags=["queries"])


@router.post("", response_model=QueryResponse, status_code=201)
def create_query(
    payload: QueryCreateRequest,
    db: Session = Depends(get_session),
    current_user: User = Depends(require_roles(Role.USER, Role.ADMIN)),
) -> QueryResponse:
    return QueryService(db).create_query(payload, current_user)


@router.get("", response_model=list[QueryResponse])
def list_queries(
    status: QueryStatus | None = QueryParam(default=None),
    priority: QueryPriority | None = QueryParam(default=None),
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[QueryResponse]:
    return QueryService(db).list_queries(current_user, status=status, priority=priority)


@router.patch("/{query_id}/assign", response_model=QueryResponse)
def assign_query(
    query_id: int,
    payload: AssignQueryRequest,
    db: Session = Depends(get_session),
    current_user: User = Depends(require_roles(Role.ADMIN)),
) -> QueryResponse:
    return QueryService(db).assign_query(query_id, payload, current_user)


@router.patch("/{query_id}/status", response_model=QueryResponse)
def update_status(
    query_id: int,
    payload: QueryStatusUpdateRequest,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> QueryResponse:
    return QueryService(db).update_status(query_id, payload, current_user)
