from typing import List, Optional
from sqlalchemy.orm import Session

from app.database.models import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


def get_device_by_id(db: Session, device_id: int) -> Optional[Device]:
    return db.query(Device).filter(Device.id == device_id).first()


def get_devices(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name_external: Optional[str] = None,
    name_internal: Optional[str] = None,
    cpu: Optional[str] = None,
    gpu: Optional[str] = None,
    ram: Optional[str] = None,
) -> List[Device]:
    query = db.query(Device)

    if name_external:
        query = query.filter(Device.name_external.ilike(f"%{name_external}%"))
    if name_internal:
        query = query.filter(Device.name_internal.ilike(f"%{name_internal}%"))
    if cpu:
        query = query.filter(Device.cpu.ilike(f"%{cpu}%"))
    if gpu:
        query = query.filter(Device.gpu.ilike(f"%{gpu}%"))
    if ram:
        query = query.filter(Device.ram.ilike(f"%{ram}%"))

    return query.offset(skip).limit(limit).all()


def create_device(db: Session, device_in: DeviceCreate) -> Device:
    db_device = Device(**device_in.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def update_device(
    db: Session,
    device_id: int,
    device_in: DeviceUpdate
) -> Optional[Device]:
    db_device = get_device_by_id(db, device_id)
    if not db_device:
        return None

    update_data = device_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_device, field, value)

    db.commit()
    db.refresh(db_device)
    return db_device
