from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester
from app.schemas.status_set import StatusSetCreate, StatusSetUpdate, StatusSetResponse
from app.services.status_set import (
    get_status_sets, get_status_set_by_id, create_status_set, update_status_set
)

router = APIRouter(prefix="/status_sets", tags=["status_sets"])


@router.get("/", response_model=List[StatusSetResponse])
def read_status_sets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    return get_status_sets(db, skip, limit)


@router.get("/{status_set_id}", response_model=StatusSetResponse)
def read_status_set(
    status_set_id: int,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    status_set = get_status_set_by_id(db, status_set_id)
    if not status_set:
        raise HTTPException(status_code=404, detail="StatusSet not found")
    return status_set


@router.post("/", response_model=StatusSetResponse, status_code=status.HTTP_201_CREATED)
def create_new_status_set(
    status_set: StatusSetCreate,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    return create_status_set(db, status_set)


@router.patch("/{status_set_id}", response_model=StatusSetResponse)
def update_existing_status_set(
    status_set_id: int,
    status_set: StatusSetUpdate,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    updated = update_status_set(db, status_set_id, status_set)
    if not updated:
        raise HTTPException(status_code=404, detail="StatusSet not found")
    return updated
