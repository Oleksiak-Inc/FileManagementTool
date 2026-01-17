from typing import Optional
from pydantic import BaseModel


class TesterTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


class TesterTypeCreate(TesterTypeBase):
    pass


class TesterTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TesterTypeResponse(TesterTypeBase):
    id: int

    class Config:
        from_attributes = True