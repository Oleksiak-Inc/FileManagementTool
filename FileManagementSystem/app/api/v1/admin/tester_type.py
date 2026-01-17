
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import require_admin
from app.database.models import Tester

from app.schemas.tester_type import (
    TesterTypeCreate,
    TesterTypeUpdate,
    TesterTypeResponse,
)
from app.services.tester_type import (
    create_tester_type,
    update_tester_type
)

router = APIRouter(prefix="/admin/tester_types", tags=["tester_types"])

@router.post("/", response_model=TesterTypeResponse, status_code=status.HTTP_201_CREATED)
def create_new_tester_type(
    tester_type: TesterTypeCreate,
    db: Session = Depends(get_db),
    current_admin: Tester = Depends(require_admin),
):
    return create_tester_type(db, tester_type)

@router.patch("/{tester_type_id}", response_model=TesterTypeResponse)
def update_existing_tester_type(
    tester_type_id: int,
    tester_type: TesterTypeUpdate,
    db: Session = Depends(get_db),
    current_admin: Tester = Depends(require_admin),
):
    updated = update_tester_type(db, tester_type_id, tester_type)
    if not updated:
        raise HTTPException(status_code=404, detail="Tester type not found")
    return updated