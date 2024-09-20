from sqlmodel import SQLModel
from typing import Optional, Dict, List


class UserContainer(SQLModel):
    web_port: int
    dns_port: int
    container_id: str
    container_name: str


class HostContainer(SQLModel):
    id: str
    name: str
    image: str
    status: str
    created: Optional[str] = None
    ports: Optional[Dict[str, str]] = None
    state: Optional[Dict[str, str]] = None
    labels: Optional[Dict[str, str]] = None
