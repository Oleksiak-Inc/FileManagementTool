from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.tester_group import (
    TesterGroupResponse,
    TesterGroupWithMembersResponse,
)
from app.services.tester_group import (
    get_tester_groups,
    get_tester_group_with_members,
)

router = APIRouter(prefix="/tester_groups", tags=["tester_groups"])


@router.get("/", response_model=List[TesterGroupResponse])
def read_tester_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    name: str | None = None,
    created_by_id: int | None = None,
    owner_id: int | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all tester groups with optional filtering."""
    return get_tester_groups(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        created_by_id=created_by_id,
        owner_id=owner_id,
    )


@router.get("/{group_id}", response_model=TesterGroupWithMembersResponse)
def read_tester_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get a specific tester group by ID with members."""
    try:
        return get_tester_group_with_members(db, group_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


