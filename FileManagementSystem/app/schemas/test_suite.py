from typing import Optional
from pydantic import BaseModel


class TestSuiteBase(BaseModel):
    name: str


class TestSuiteCreate(TestSuiteBase):
    pass


class TestSuiteUpdate(BaseModel):
    name: Optional[str] = None


class TestSuiteResponse(TestSuiteBase):
    id: int

    class Config:
        from_attributes = True
