from pydantic import BaseModel


class Container(BaseModel):
    container_name: str
    host_name: str
