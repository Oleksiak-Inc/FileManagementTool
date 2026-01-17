from typing import Optional
from pydantic import BaseModel


class StatusSetBase(BaseModel):
    name: str


class StatusSetCreate(StatusSetBase):
    pass


class StatusSetUpdate(BaseModel):
    name: Optional[str] = None


class StatusSetResponse(StatusSetBase):
    id: int

    class Config:
        from_attributes = True
