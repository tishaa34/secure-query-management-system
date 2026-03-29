from app.core.enums import Role
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.modules.users.models import User


def seed_users() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        existing_names = {user.name for user in session.query(User).all()}
        seed_set = [
            ("admin", Role.ADMIN),
            ("resolver1", Role.RESOLVER),
            ("resolver2", Role.RESOLVER),
            ("reporter1", Role.USER),
            ("reporter2", Role.USER),
        ]

        for name, role in seed_set:
            if name not in existing_names:
                session.add(User(name=name, role=role))

        session.commit()


if __name__ == "__main__":
    seed_users()
