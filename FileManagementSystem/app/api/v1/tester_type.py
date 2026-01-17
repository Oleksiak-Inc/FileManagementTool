from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester
from app.schemas.tester_type import (
    TesterTypeCreate,
    TesterTypeUpdate,
    TesterTypeResponse,
)
from app.services.tester_type import (
    get_tester_types,
    get_tester_type_by_id,
    create_tester_type,
    update_tester_type
)

router = APIRouter(prefix="/tester_types", tags=["tester_types"])  # Changed prefix


@router.get("/", response_model=List[TesterTypeResponse])
def read_tester_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    return get_tester_types(db, skip, limit)


@router.get("/{tester_type_id}", response_model=TesterTypeResponse)  # Changed parameter name
def read_tester_type(
    tester_type_id: int,  # Changed parameter name
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    tester_type = get_tester_type_by_id(db, tester_type_id)
    if not tester_type:
        raise HTTPException(status_code=404, detail="Tester type not found")
    return tester_type


@router.post("/", response_model=TesterTypeResponse, status_code=status.HTTP_201_CREATED)
def create_new_tester_type(
    tester_type: TesterTypeCreate,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    return create_tester_type(db, tester_type)