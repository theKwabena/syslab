from sqlmodel import Session, select
from schemas.user import UserCreate
from models.user import User
from pydantic import EmailStr
from fastapi import Query


class UserService:

    def __init__(self, session: Session):
        self.session = session

    def user_exists(self, email: str) -> bool:
        user = self.session.get(User, email)
        if user is None:
            return False
        return True

    @staticmethod
    def create_user(self, user: UserCreate):
        db_user = User.model_validate(user)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(self, username: str) -> User:
        user = self.session.get(User, username)
        if not user:
            pass

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
        self.session.flush()
        self.session.refresh(user)
        return user


class UnixLabContainerService:
    pass
