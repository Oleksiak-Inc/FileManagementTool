from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.tester import TesterResponse, TesterCreate, TesterUpdate
from app.services.tester import (
    get_tester_by_id, 
    get_tester_by_email, 
    get_testers, 
    create_tester, 
    update_tester, 
    create_tester_self, 
    create_tester_admin
)

router = APIRouter(prefix="/testers", tags=["testers"])

@router.get("/", response_model=List[TesterResponse])
def read_testers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    email: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    active: bool | None = None,
    tester_type_id: int | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    return get_testers(
        db=db,
        skip=skip,
        limit=limit,
        email=email,
        first_name=first_name,
        last_name=last_name,
        active=active,
        tester_type_id=tester_type_id,
    )


@router.get("/me", response_model=TesterResponse)
def read_tester_me(current_tester: TesterModel = Depends(get_current_tester)):
    """Get current tester"""
    return current_tester

@router.get("/{tester_id}", response_model=TesterResponse)
def read_tester(
    tester_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester)
):
    """Get specific tester by ID"""
    db_tester = get_tester_by_id(db, tester_id=tester_id)
    if db_tester is None:
        raise HTTPException(status_code=404, detail="Tester not found")
    return db_tester

@router.post("/register", response_model=TesterResponse)
def register_tester(
    payload: TesterCreate,
    db: Session = Depends(get_db),
):
    return create_tester_self(db, payload)

@router.patch("/{tester_id}", response_model=TesterResponse)
def update_existing_tester(
    tester_id: int,
    tester: TesterUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester)
):
    """Update tester"""
    db_tester = update_tester(db, tester_id, tester)
    if db_tester is None:
        raise HTTPException(status_code=404, detail="Tester not found")
    return db_tester