from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class TesterBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class TesterCreate(TesterBase):
    password: str

class TesterUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    # tester_type_id: Optional[int] = None
    # active: Optional[bool] = None

class TesterAdminUpdate(TesterUpdate):
    tester_type_id: Optional[int] = None
    tester_group_id: Optional[int] = None
    active: Optional[bool] = None

class TesterResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    tester_type_id: int
    active: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TesterInDB(TesterResponse):
    password: str


class TesterCreateAdmin(TesterCreate):
    tester_type_id: Optional[int] = None
    tester_group_id: Optional[int] = None
    active: Optional[bool] = True
