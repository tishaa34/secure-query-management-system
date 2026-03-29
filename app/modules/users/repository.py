from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.users.models import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_name(self, name: str) -> User | None:
        statement = select(User).where(User.name == name)
        return self.db.scalar(statement)

    def list_all(self) -> list[User]:
        statement = select(User).order_by(User.id)
        return list(self.db.scalars(statement).all())
