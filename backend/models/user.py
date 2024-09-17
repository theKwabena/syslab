from .container import Container
from sqlmodel import Relationship, Field, SQLModel


class User(SQLModel, table=True):
    password: str
    username: str = Field(default=None, primary_key=True)
    is_admin: bool = Field(default=False)

    container_id: int | None = Field(default=None, foreign_key="container.id")
    container: Container | None = Relationship(back_populates="users")
