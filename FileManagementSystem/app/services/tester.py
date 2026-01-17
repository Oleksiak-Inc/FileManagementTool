from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database.models import Tester, TesterType
from app.utils.auth import hash_password
from app.schemas.tester import TesterCreate, TesterUpdate, TesterCreateAdmin

def get_tester_by_id(db: Session, tester_id: int) -> Optional[Tester]:
    return db.query(Tester).filter(Tester.id == tester_id).first()

def get_tester_by_email(db: Session, tester_email: str) -> Optional[Tester]:
    return db.query(Tester).filter(Tester.email == tester_email).first()

def get_testers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    active: Optional[bool] = None,
    tester_type_id: Optional[int] = None,
) -> List[Tester]:
    query = db.query(Tester)

    if active is not None:
        query = query.filter(Tester.active == active)

    if tester_type_id is not None:
        query = query.filter(Tester.tester_type_id == tester_type_id)

    if email:
        query = query.filter(Tester.email.ilike(f"%{email}%"))

    if first_name:
        query = query.filter(Tester.first_name.ilike(f"%{first_name}%"))

    if last_name:
        query = query.filter(Tester.last_name.ilike(f"%{last_name}%"))

    return query.offset(skip).limit(limit).all()

def create_tester(db: Session, tester_in: TesterCreate) -> Tester:
    tester_type = db.query(TesterType).filter_by(name="regular").first()

    if not tester_type:
        raise ValueError("Invalid tester type")

    db_tester = Tester(
        email=tester_in.email,
        first_name=tester_in.first_name,
        last_name=tester_in.last_name,
        password=hash_password(tester_in.password),
        tester_type_id=tester_type.id,
    )
    db.add(db_tester)
    db.commit()
    db.refresh(db_tester)
    return db_tester


def create_tester_self(db: Session, data: TesterCreate) -> Tester:
    regular_type = db.query(TesterType).filter_by(id=3).one()

    tester = Tester(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password=hash_password(data.password),
        tester_type_id=regular_type.id,
        active=True,
    )
    db.add(tester)
    db.commit()
    db.refresh(tester)
    return tester


def create_tester_admin(db: Session, data: TesterCreateAdmin) -> Tester:
    tester = Tester(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password=hash_password(data.password),
        tester_type_id=data.tester_type_id or 3,
        tester_group_id=data.tester_group_id,
        active=data.active if data.active is not None else True,
    )
    db.add(tester)
    db.commit()
    db.refresh(tester)
    return tester


def update_tester(db: Session, tester_id: int, tester_in: TesterUpdate) -> Optional[Tester]:
    db_tester = get_tester_by_id(db, tester_id)
    if not db_tester:
        return None
    
    update_data = tester_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tester, field, value)
    
    db.commit()
    db.refresh(db_tester)
    return db_tester