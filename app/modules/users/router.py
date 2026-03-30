from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_session, require_roles
from app.core.enums import Role
from app.modules.users.schemas import UserCreateRequest, UserResponse
from app.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(
    payload: UserCreateRequest,
    db: Session = Depends(get_session),
    _: object = Depends(require_roles(Role.ADMIN)),
) -> UserResponse:
    return UserService(db).create_user(payload)


@router.get("", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_session),
    _: object = Depends(require_roles(Role.ADMIN)),
) -> list[UserResponse]:
    return UserService(db).list_users()
