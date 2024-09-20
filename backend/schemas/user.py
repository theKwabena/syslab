from sqlmodel import SQLModel
from .container import UserContainer

class UserBase(SQLModel):
    username: str | None = None


class UserCreate(SQLModel):
    username: str
    password: str


class UserRead(UserBase):
    username: str
    container: UserContainer | None = None
