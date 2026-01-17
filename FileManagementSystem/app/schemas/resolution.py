from typing import Optional
from pydantic import BaseModel


class ResolutionBase(BaseModel):
    w: int
    h: int


class ResolutionCreate(ResolutionBase):
    pass


class ResolutionUpdate(BaseModel):
    w: Optional[int] = None
    h: Optional[int] = None


class ResolutionResponse(ResolutionBase):
    id: int

    class Config:
        from_attributes = True
