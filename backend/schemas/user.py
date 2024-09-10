from sqlmodel import SQLModel


class UserBase(SQLModel):
    username: str | None = None


class UserCreate(SQLModel):
    username: str
    password: str


class UserRead(UserBase):
    username: str
