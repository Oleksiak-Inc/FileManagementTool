from typing import List, Optional
from sqlalchemy.orm import Session

from app.database.models import TesterType
from app.schemas.tester_type import TesterTypeCreate, TesterTypeUpdate


def get_tester_type_by_id(db: Session, tester_type_id: int) -> Optional[TesterType]:
    return db.query(TesterType).filter(TesterType.id == tester_type_id).first()


def get_tester_type_by_name(db: Session, name: str) -> Optional[TesterType]:
    return db.query(TesterType).filter(TesterType.name == name).first()


def get_tester_types(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> List[TesterType]:
    return db.query(TesterType).offset(skip).limit(limit).all()


def create_tester_type(db: Session, tester_type_in: TesterTypeCreate) -> TesterType:
    tester_type = TesterType(**tester_type_in.dict())
    db.add(tester_type)
    db.commit()
    db.refresh(tester_type)
    return tester_type


def update_tester_type(
    db: Session,
    tester_type_id: int,
    tester_type_in: TesterTypeUpdate,
) -> Optional[TesterType]:
    tester_type = get_tester_type_by_id(db, tester_type_id)
    if not tester_type:
        return None

    for field, value in tester_type_in.dict(exclude_unset=True).items():
        setattr(tester_type, field, value)

    db.commit()
    db.refresh(tester_type)
    return tester_type
