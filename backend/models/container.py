from typing import List
from sqlmodel import Relationship, Field, SQLModel


class Container(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    host_name: str
    web_port: int
    dns_port: int
    container_id: str
    container_name: str
    user: "User" = Relationship(back_populates="container")
