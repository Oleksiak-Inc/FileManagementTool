# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/schemas/test_case.py ---
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class TestCaseBase(BaseModel):
    scenario_id: int
    status_set_id: int


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseUpdate(BaseModel):
    scenario_id: Optional[int] = None
    status_set_id: Optional[int] = None


class TestCaseResponse(TestCaseBase):
    id: int

    class Config:
        from_attributes = True


# Extended response that includes related objects
class TestCaseWithRelationsResponse(BaseModel):
    id: int
    scenario_id: int
    status_set_id: int
    # You can add relationships here if needed
    # scenario: Optional[ScenarioResponse] = None
    # status_set: Optional[StatusSetResponse] = None
    
    class Config:
        from_attributes = True