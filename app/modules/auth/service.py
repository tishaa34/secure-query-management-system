from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError
from app.core.security import create_access_token
from app.modules.auth.schemas import LoginRequest, LoginResponse
from app.modules.users.repository import UserRepository


class AuthService:
    def __init__(self, db: Session) -> None:
        self.user_repository = UserRepository(db)

    def login(self, payload: LoginRequest) -> LoginResponse:
        user = self.user_repository.get_by_name(payload.name)
        if user is None:
            raise AuthenticationError("Unknown user. Seed users first or create one in the database.")

        return LoginResponse(
            access_token=create_access_token(user.id),
            user_id=user.id,
            role=user.role,
        )
