from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.device import (
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse,
)
from app.services.device import (
    get_devices,
    get_device_by_id,
    create_device,
    update_device
)

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=List[DeviceResponse])
def read_devices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    name_external: str | None = None,
    name_internal: str | None = None,
    cpu: str | None = None,
    gpu: str | None = None,
    ram: str | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    return get_devices(
        db=db,
        skip=skip,
        limit=limit,
        name_external=name_external,
        name_internal=name_internal,
        cpu=cpu,
        gpu=gpu,
        ram=ram,
    )


@router.get("/{device_id}", response_model=DeviceResponse)
def read_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    device = get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_new_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    return create_device(db, device)


@router.patch("/{device_id}", response_model=DeviceResponse)
def update_existing_device(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    updated = update_device(db, device_id, device)
    if not updated:
        raise HTTPException(status_code=404, detail="Device not found")
    return updated