# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/schemas/status.py ---
from typing import Optional
from pydantic import BaseModel


class StatusBase(BaseModel):
    name: str
    description: Optional[str] = None
    status_set_id: int


class StatusCreate(StatusBase):
    pass


class StatusUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status_set_id: Optional[int] = None


class StatusResponse(StatusBase):
    id: int

    class Config:
        from_attributes = True