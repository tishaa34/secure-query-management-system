from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.enums import Role
from app.core.exceptions import AuthorizationError
from app.core.security import get_current_user
from app.db.session import get_db
from app.modules.users.models import User


def require_roles(*roles: Role) -> Callable[[User], User]:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise AuthorizationError("You do not have access to this resource.")
        return current_user

    return dependency


def get_session(db: Session = Depends(get_db)) -> Session:
    return db
