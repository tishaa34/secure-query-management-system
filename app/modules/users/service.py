from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.modules.users.models import User
from app.modules.users.repository import UserRepository


class UserService:
    def __init__(self, db: Session) -> None:
        self.user_repository = UserRepository(db)

    def get_user_or_fail(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} was not found.")
        return user
