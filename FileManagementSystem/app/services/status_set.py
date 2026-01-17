from typing import List, Optional
from sqlalchemy.orm import Session

from app.database.models import StatusSet
from app.schemas.status_set import StatusSetCreate, StatusSetUpdate


def get_status_set_by_id(db: Session, status_set_id: int) -> Optional[StatusSet]:
    return db.query(StatusSet).filter(StatusSet.id == status_set_id).first()


def get_status_sets(db: Session, skip: int = 0, limit: int = 100) -> List[StatusSet]:
    return db.query(StatusSet).offset(skip).limit(limit).all()


def create_status_set(db: Session, status_set_in: StatusSetCreate) -> StatusSet:
    status_set = StatusSet(**status_set_in.dict())
    db.add(status_set)
    db.commit()
    db.refresh(status_set)
    return status_set


def update_status_set(db: Session, status_set_id: int, status_set_in: StatusSetUpdate) -> Optional[StatusSet]:
    status_set = get_status_set_by_id(db, status_set_id)
    if not status_set:
        return None

    for field, value in status_set_in.dict(exclude_unset=True).items():
        setattr(status_set, field, value)

    db.commit()
    db.refresh(status_set)
    return status_set
