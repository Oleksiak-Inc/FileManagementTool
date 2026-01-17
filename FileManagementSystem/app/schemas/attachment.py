# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/schemas/attachment.py ---
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AttachmentBase(BaseModel):
    parent_attachment_id: Optional[int] = None
    resolution_id: Optional[int] = None
    filename: str
    relative_path: str
    presentmon_file: bool = False
    presentmon_version: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class AttachmentCreate(AttachmentBase):
    uploaded_by: int


class AttachmentUpdate(BaseModel):
    parent_attachment_id: Optional[int] = None
    resolution_id: Optional[int] = None
    filename: Optional[str] = None
    relative_path: Optional[str] = None
    presentmon_file: Optional[bool] = None
    presentmon_version: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class AttachmentResponse(AttachmentBase):
    id: int
    uploaded_by: int
    uploaded_at: datetime
    parent_attachment_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class AttachmentWithRelationsResponse(AttachmentResponse):
    uploader: Optional[Dict[str, Any]] = None
    resolution: Optional[Dict[str, Any]] = None
    parent: Optional[Dict[str, Any]] = None
    children: Optional[list] = None
    
    class Config:
        from_attributes = True


class FileUploadResponse(BaseModel):
    message: str
    attachment_id: int
    filename: str
    file_path: str
    file_url: str


class AttachmentFilter(BaseModel):
    filename: Optional[str] = None
    uploaded_by: Optional[int] = None
    resolution_id: Optional[int] = None
    parent_attachment_id: Optional[int] = None
    presentmon_file: Optional[bool] = None