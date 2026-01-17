from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester, require_admin
from app.database.models import Tester
from app.schemas.tester_group import (
    TesterGroupCreate,
    TesterGroupUpdate,
    TesterGroupResponse,
    TesterGroupWithMembersResponse,
    AddMemberRequest,
    BulkAddMembersRequest
)
from app.services.tester_group import (
    get_tester_groups,
    create_tester_group,
    update_tester_group,
    get_tester_group_with_members,
    add_member_to_group,
    add_multiple_members_to_group,
)

router = APIRouter(prefix="/admin/tester_groups", tags=["tester_groups"])


@router.post("/", response_model=TesterGroupResponse, status_code=status.HTTP_201_CREATED)
def create_new_tester_group(
    group_data: TesterGroupCreate,
    db: Session = Depends(get_db),
    current_admin: Tester = Depends(require_admin),
):
    """Create a new tester group."""
    try:
        return create_tester_group(db, group_data, current_admin.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{group_id}", response_model=TesterGroupResponse)
def update_existing_tester_group(
    group_id: int,
    group_data: TesterGroupUpdate,
    db: Session = Depends(get_db),
    current_admin: Tester = Depends(require_admin),
):
    """Update an existing tester group."""
    try:
        updated = update_tester_group(db, group_id, group_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Tester group not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{group_id}/members", response_model=dict)
def add_member(
    group_id: int,
    request: AddMemberRequest,
    db: Session = Depends(get_db),
    current_admin: Tester = Depends(require_admin),
):
    """Add a tester to a tester group."""
    try:
        tester = add_member_to_group(db, group_id, request.tester_id)
        return {
            "message": "Member added successfully",
            "tester_id": tester.id,
            "group_id": group_id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{group_id}/members/bulk", response_model=dict)
def add_multiple_members(
    group_id: int,
    request: BulkAddMembersRequest,
    db: Session = Depends(get_db),
    current_admin: Tester = Depends(require_admin),
):
    """Add multiple testers to a tester group."""
    try:
        testers = add_multiple_members_to_group(db, group_id, request.tester_ids)
        return {
            "message": f"Added {len(testers)} members to group",
            "added_count": len(testers),
            "group_id": group_id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

