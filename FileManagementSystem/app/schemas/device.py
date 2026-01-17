from typing import Optional
from pydantic import BaseModel


class DeviceBase(BaseModel):
    name_external: str
    name_internal: str
    cpu: str
    gpu: str
    ram: str
    project_id: int


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name_external: Optional[str] = None
    name_internal: Optional[str] = None
    cpu: Optional[str] = None
    gpu: Optional[str] = None
    ram: Optional[str] = None
    project_id: Optional[int] = None


class DeviceResponse(DeviceBase):
    id: int

    class Config:
        from_attributes = True
