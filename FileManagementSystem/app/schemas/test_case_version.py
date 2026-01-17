# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/schemas/test_case_version.py ---
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TestCaseVersionBase(BaseModel):
    test_case_id: int
    created_by: int
    release_ready: bool = False
    name: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[str] = None
    expected_result: Optional[str] = None


class TestCaseVersionCreate(TestCaseVersionBase):
    # Version is auto-incremented, so not in create schema
    pass


class TestCaseVersionUpdate(BaseModel):
    release_ready: Optional[bool] = None
    name: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[str] = None
    expected_result: Optional[str] = None


class TestCaseVersionResponse(TestCaseVersionBase):
    id: int
    version: int
    created_at: datetime

    class Config:
        from_attributes = True


# Extended response that includes related objects
class TestCaseVersionWithRelationsResponse(BaseModel):
    id: int
    test_case_id: int
    created_by: int
    version: int
    release_ready: bool
    name: Optional[str]
    description: Optional[str]
    steps: Optional[str]
    expected_result: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Response for creating a new version (includes version number)
class TestCaseVersionCreateResponse(BaseModel):
    id: int
    test_case_id: int
    created_by: int
    version: int
    release_ready: bool
    name: Optional[str]
    description: Optional[str]
    steps: Optional[str]
    expected_result: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True