from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.resolution import (
    ResolutionCreate,
    ResolutionUpdate,
    ResolutionResponse,
)
from app.services.resolution import (
    get_resolutions,
    get_resolution_by_id,
    create_resolution,
    update_resolution
)

router = APIRouter(prefix="/resolutions", tags=["resolutions"])


@router.get("/", response_model=List[ResolutionResponse])
def read_resolutions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    w: int | None = None,
    h: int | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    return get_resolutions(
        db=db,
        skip=skip,
        limit=limit,
        w=w,
        h=h,
    )


@router.get("/{resolution_id}", response_model=ResolutionResponse)
def read_resolution(
    resolution_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    resolution = get_resolution_by_id(db, resolution_id)
    if not resolution:
        raise HTTPException(status_code=404, detail="Resolution not found")
    return resolution


@router.post("/", response_model=ResolutionResponse, status_code=status.HTTP_201_CREATED)
def create_new_resolution(
    resolution: ResolutionCreate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    try:
        return create_resolution(db, resolution)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{resolution_id}", response_model=ResolutionResponse)
def update_existing_resolution(
    resolution_id: int,
    resolution: ResolutionUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    updated = update_resolution(db, resolution_id, resolution)
    if not updated:
        raise HTTPException(status_code=404, detail="Resolution not found")
    return updated