from typing import List
from sqlmodel import Relationship, Field, SQLModel


class Container(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    container_name: str
    host_name: str
    users: List["User"] = Relationship(back_populates="container")
