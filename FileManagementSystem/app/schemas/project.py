from typing import Optional
from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    client_id: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    client_id: Optional[int] = None


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True
