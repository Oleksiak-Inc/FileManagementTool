from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import Tester as TesterModel
from app.schemas.tester import TesterCreateAdmin, TesterResponse
from app.services.tester import create_tester_admin
from app.api.dependencies import require_admin

router = APIRouter(prefix="/admin/testers", tags=["admin"])

@router.post("", response_model=TesterResponse, status_code=status.HTTP_201_CREATED)
def admin_create_tester(
    payload: TesterCreateAdmin,
    db: Session = Depends(get_db),
    current_admin: TesterModel = Depends(require_admin),  # Proper dependency
):
    """Create a new tester (admin only)"""
    return create_tester_admin(db, payload)