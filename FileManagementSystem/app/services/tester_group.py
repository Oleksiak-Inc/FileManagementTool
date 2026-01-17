from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.models import TesterGroup, Tester
from app.schemas.tester_group import TesterGroupCreate, TesterGroupUpdate


def get_tester_group_by_id(db: Session, group_id: int) -> Optional[TesterGroup]:
    """Get a single tester group by ID."""
    return db.query(TesterGroup).filter(TesterGroup.id == group_id).first()


def get_tester_groups(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    created_by_id: Optional[int] = None,
    owner_id: Optional[int] = None,
) -> List[TesterGroup]:
    """Get multiple tester groups with optional filtering."""
    query = db.query(TesterGroup)

    if name:
        query = query.filter(TesterGroup.name.ilike(f"%{name}%"))
    if created_by_id is not None:
        query = query.filter(TesterGroup.created_by_id == created_by_id)
    if owner_id is not None:
        query = query.filter(TesterGroup.owner_id == owner_id)

    return query.order_by(TesterGroup.name).offset(skip).limit(limit).all()


def create_tester_group(db: Session, group_in: TesterGroupCreate, created_by_id: int) -> TesterGroup:
    """Create a new tester group."""
    # Check if owner exists
    owner_id = group_in.owner_id or created_by_id
    owner = db.query(Tester).filter(Tester.id == owner_id).first()
    if not owner:
        raise ValueError(f"Tester with ID {owner_id} does not exist")
    
    # Check if group name already exists
    existing_group = db.query(TesterGroup).filter(TesterGroup.name == group_in.name).first()
    if existing_group:
        raise ValueError(f"Tester group with name '{group_in.name}' already exists")
    
    group_data = {
        "name": group_in.name,
        "created_by_id": created_by_id,
        "owner_id": owner_id
    }
    
    group = TesterGroup(**group_data)
    db.add(group)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise ValueError("Invalid foreign key reference")
        else:
            raise ValueError(f"Database error: {e}")
    
    db.refresh(group)
    return group


def update_tester_group(
    db: Session,
    group_id: int,
    group_in: TesterGroupUpdate,
) -> Optional[TesterGroup]:
    """Update an existing tester group."""
    group = get_tester_group_by_id(db, group_id)
    if not group:
        return None

    update_data = group_in.dict(exclude_unset=True)
    
    # Validate owner if being updated
    if "owner_id" in update_data and update_data["owner_id"]:
        owner = db.query(Tester).filter(Tester.id == update_data["owner_id"]).first()
        if not owner:
            raise ValueError(f"Tester with ID {update_data['owner_id']} does not exist")

    for field, value in update_data.items():
        setattr(group, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise ValueError("Invalid foreign key reference")
        else:
            raise ValueError(f"Database error: {e}")
    
    db.refresh(group)
    return group


def get_tester_group_with_members(db: Session, group_id: int) -> Dict[str, Any]:
    """Get a tester group with all its members and owner/creator info."""
    group = db.query(TesterGroup).filter(TesterGroup.id == group_id).first()
    if not group:
        raise ValueError(f"Tester group with ID {group_id} does not exist")
    
    return {
        "id": group.id,
        "name": group.name,
        "created_by": {
            "id": group.created_by.id,
            "email": group.created_by.email,
            "first_name": group.created_by.first_name,
            "last_name": group.created_by.last_name
        } if group.created_by else None,
        "owner": {
            "id": group.owner.id,
            "email": group.owner.email,
            "first_name": group.owner.first_name,
            "last_name": group.owner.last_name
        } if group.owner else None,
        "members": [
            {
                "id": member.id,
                "email": member.email,
                "first_name": member.first_name,
                "last_name": member.last_name,
                "tester_type_id": member.tester_type_id,
                "active": member.active
            }
            for member in group.members
        ] if group.members else []
    }


def add_member_to_group(db: Session, group_id: int, tester_id: int) -> Tester:
    """Add a tester to a tester group."""
    group = get_tester_group_by_id(db, group_id)
    if not group:
        raise ValueError(f"Tester group with ID {group_id} does not exist")
    
    tester = db.query(Tester).filter(Tester.id == tester_id).first()
    if not tester:
        raise ValueError(f"Tester with ID {tester_id} does not exist")
    
    # Check if tester is already in the group
    if tester.tester_group_id == group_id:
        raise ValueError(f"Tester {tester_id} is already in group {group_id}")
    
    tester.tester_group_id = group_id
    db.commit()
    db.refresh(tester)
    return tester


def remove_member_from_group(db: Session, group_id: int, tester_id: int) -> bool:
    """Remove a tester from a tester group."""
    group = get_tester_group_by_id(db, group_id)
    if not group:
        return False
    
    tester = db.query(Tester).filter(Tester.id == tester_id).first()
    if not tester:
        return False
    
    if tester.tester_group_id != group_id:
        return False
    
    tester.tester_group_id = None
    db.commit()
    return True


def add_multiple_members_to_group(db: Session, group_id: int, tester_ids: List[int]) -> List[Tester]:
    """Add multiple testers to a tester group."""
    results = []
    
    for tester_id in tester_ids:
        try:
            tester = add_member_to_group(db, group_id, tester_id)
            results.append(tester)
        except ValueError as e:
            # Skip duplicates and continue with others
            continue
    
    return results


def remove_all_members_from_group(db: Session, group_id: int) -> int:
    """Remove all members from a tester group."""
    group = get_tester_group_by_id(db, group_id)
    if not group:
        return 0
    
    # Get all members in this group
    members = db.query(Tester).filter(Tester.tester_group_id == group_id).all()
    
    for member in members:
        member.tester_group_id = None
    
    db.commit()
    return len(members)