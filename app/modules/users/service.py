from sqlalchemy.orm import Session

from app.core.exceptions import ValidationError, NotFoundError
from app.modules.users.models import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreateRequest


class UserService:
    def __init__(self, db: Session) -> None:
        self.user_repository = UserRepository(db)

    def get_user_or_fail(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} was not found.")
        return user

    def create_user(self, payload: UserCreateRequest) -> User:
        if self.user_repository.get_by_name(payload.name) is not None:
            raise ValidationError(f"User '{payload.name}' already exists.")

        user = User(name=payload.name, role=payload.role)
        created_user = self.user_repository.create(user)
        self.user_repository.db.commit()
        return created_user

    def list_users(self) -> list[User]:
        return self.user_repository.list_all()
