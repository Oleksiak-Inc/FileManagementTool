from typing import Optional
from pydantic import BaseModel


class ScenarioBase(BaseModel):
    name: str


class ScenarioCreate(ScenarioBase):
    pass


class ScenarioUpdate(BaseModel):
    name: Optional[str] = None


class ScenarioResponse(ScenarioBase):
    id: int

    class Config:
        from_attributes = True
