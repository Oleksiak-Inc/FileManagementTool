from typing import Optional
from pydantic import BaseModel


class ClientBase(BaseModel):
    name: str


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None


class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True
