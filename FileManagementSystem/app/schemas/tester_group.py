from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class TesterGroupBase(BaseModel):
    name: str
    created_by_id: int
    owner_id: int


class TesterGroupCreate(BaseModel):
    name: str
    owner_id: Optional[int] = None


class TesterGroupUpdate(BaseModel):
    name: Optional[str] = None
    owner_id: Optional[int] = None


class TesterGroupResponse(TesterGroupBase):
    id: int
    
    class Config:
        from_attributes = True


class TesterGroupWithMembersResponse(TesterGroupResponse):
    created_by: Optional[dict] = None
    owner: Optional[dict] = None
    members: Optional[List[dict]] = None
    
    class Config:
        from_attributes = True


class AddMemberRequest(BaseModel):
    tester_id: int


class RemoveMemberRequest(BaseModel):
    tester_id: int


class BulkAddMembersRequest(BaseModel):
    tester_ids: List[int]