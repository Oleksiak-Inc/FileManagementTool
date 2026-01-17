from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.models import Resolution
from app.schemas.resolution import ResolutionCreate, ResolutionUpdate


def get_resolution_by_id(db: Session, resolution_id: int) -> Optional[Resolution]:
    return db.query(Resolution).filter(Resolution.id == resolution_id).first()


def get_resolutions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    w: Optional[int] = None,
    h: Optional[int] = None,
) -> List[Resolution]:
    query = db.query(Resolution)

    if w is not None:
        query = query.filter(Resolution.w == w)
    if h is not None:
        query = query.filter(Resolution.h == h)

    return query.offset(skip).limit(limit).all()


def create_resolution(db: Session, resolution_in: ResolutionCreate) -> Resolution:
    resolution = Resolution(**resolution_in.dict())
    db.add(resolution)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Resolution with same width and height already exists")

    db.refresh(resolution)
    return resolution


def update_resolution(
    db: Session,
    resolution_id: int,
    resolution_in: ResolutionUpdate,
) -> Optional[Resolution]:
    resolution = get_resolution_by_id(db, resolution_id)
    if not resolution:
        return None

    update_data = resolution_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resolution, field, value)

    db.commit()
    db.refresh(resolution)
    return resolution

