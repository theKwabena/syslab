from sqlmodel import Session, select
from schemas.user import UserCreate
from models.user import User
from pydantic import EmailStr
from fastapi import Query

from config.security import verify_password, get_password_hash


class UserService:

    def __init__(self, session: Session):
        self.session = session

    def user_exists(self, email: str) -> bool:
        user = self.session.get(User, email)
        if user is None:
            return False
        return True

    def create_user(self, user: UserCreate, is_admin: bool):
        db_user = User.model_validate(
            user, update={"password": get_password_hash(user.password)}
        )
        db_user.is_admin = is_admin
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_user(self, username: str) -> User | None:
        user = self.session.get(User, username)
        return user

    def get_users(
            self,
            offset: int = 0,
            limit: int = Query(default=100, le=100),
    ):
        users = self.session.exec(select(User)).all()
        return users

    def delete_user(self, user_email: EmailStr):
        user = self.session.get(User, user_email)
        if not user:
            pass
        self.session.delete(user)
        self.session.commit()
        return 'Ok'

    def get_user_container(self, user_email: EmailStr):
        user: User | None = self.session.get(User, user_email)
        if not user:
            pass
        return user.container

    def update_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.get_user(email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


class UnixLabContainerService:
    pass
