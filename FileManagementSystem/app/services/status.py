# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/services/status.py ---
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.models import Status
from app.schemas.status import StatusCreate, StatusUpdate


def get_status_by_id(db: Session, status_id: int) -> Optional[Status]:
    """Get a single status by ID."""
    return db.query(Status).filter(Status.id == status_id).first()


def get_statuses(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    status_set_id: Optional[int] = None,
) -> List[Status]:
    """Get multiple statuses with optional filtering."""
    query = db.query(Status)

    if name:
        query = query.filter(Status.name.ilike(f"%{name}%"))
    if status_set_id is not None:
        query = query.filter(Status.status_set_id == status_set_id)

    return query.offset(skip).limit(limit).all()


def create_status(db: Session, status_in: StatusCreate) -> Status:
    """Create a new status."""
    status = Status(**status_in.dict())
    db.add(status)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Check if it's a foreign key violation
        if "foreign key constraint" in str(e).lower():
            raise ValueError(f"Invalid status_set_id: {status_in.status_set_id}")
        # Check if it's a duplicate name within the same status set
        elif "unique constraint" in str(e).lower():
            raise ValueError(f"Status with name '{status_in.name}' already exists in this status set")
        else:
            raise
    db.refresh(status)
    return status


def update_status(
    db: Session,
    status_id: int,
    status_in: StatusUpdate,
) -> Optional[Status]:
    """Update an existing status."""
    status = get_status_by_id(db, status_id)
    if not status:
        return None

    update_data = status_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(status, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise ValueError(f"Invalid status_set_id: {status_in.status_set_id}")
        elif "unique constraint" in str(e).lower():
            raise ValueError(f"Status with updated name already exists in this status set")
        else:
            raise
    
    db.refresh(status)
    return status