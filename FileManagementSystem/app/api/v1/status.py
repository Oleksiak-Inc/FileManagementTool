# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/api/v1/status.py ---
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.status import StatusCreate, StatusUpdate, StatusResponse
from app.services.status import (
    get_statuses,
    get_status_by_id,
    create_status,
    update_status
)

router = APIRouter(prefix="/statuses", tags=["statuses"])


@router.get("/", response_model=List[StatusResponse])
def read_statuses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    name: str | None = None,
    status_set_id: int | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all statuses with optional filtering."""
    return get_statuses(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        status_set_id=status_set_id,
    )


@router.get("/{status_id}", response_model=StatusResponse)
def read_status(
    status_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get a specific status by ID."""
    status = get_status_by_id(db, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status


@router.post("/", response_model=StatusResponse, status_code=status.HTTP_201_CREATED)
def create_new_status(
    status_data: StatusCreate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Create a new status."""
    try:
        return create_status(db, status_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{status_id}", response_model=StatusResponse)
def update_existing_status(
    status_id: int,
    status_data: StatusUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Update an existing status."""
    try:
        updated = update_status(db, status_id, status_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Status not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
