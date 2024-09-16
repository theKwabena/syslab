from pydantic import BaseModel, constr


class ProxyBackend(BaseModel):
    name: str
    mode: constr()
    balance: dict
