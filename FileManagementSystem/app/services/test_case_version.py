# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/services/test_case_version.py ---
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, and_

from app.database.models import TestCaseVersion, TestCase, Tester
from app.schemas.test_case_version import TestCaseVersionCreate, TestCaseVersionUpdate


def get_test_case_version_by_id(db: Session, version_id: int) -> Optional[TestCaseVersion]:
    """Get a single test case version by ID."""
    return db.query(TestCaseVersion).filter(TestCaseVersion.id == version_id).first()


def get_test_case_versions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    test_case_id: Optional[int] = None,
    created_by: Optional[int] = None,
    release_ready: Optional[bool] = None,
    version: Optional[int] = None,
) -> List[TestCaseVersion]:
    """Get multiple test case versions with optional filtering."""
    query = db.query(TestCaseVersion)

    if test_case_id is not None:
        query = query.filter(TestCaseVersion.test_case_id == test_case_id)
    if created_by is not None:
        query = query.filter(TestCaseVersion.created_by == created_by)
    if release_ready is not None:
        query = query.filter(TestCaseVersion.release_ready == release_ready)
    if version is not None:
        query = query.filter(TestCaseVersion.version == version)

    return query.order_by(desc(TestCaseVersion.version)).offset(skip).limit(limit).all()


def get_latest_version_for_test_case(db: Session, test_case_id: int) -> Optional[TestCaseVersion]:
    """Get the latest version for a specific test case."""
    return db.query(TestCaseVersion).filter(
        TestCaseVersion.test_case_id == test_case_id
    ).order_by(desc(TestCaseVersion.version)).first()


def get_next_version_number(db: Session, test_case_id: int) -> int:
    """Get the next version number for a test case."""
    latest_version = get_latest_version_for_test_case(db, test_case_id)
    if latest_version:
        return latest_version.version + 1
    return 1  # First version


def create_test_case_version(db: Session, version_in: TestCaseVersionCreate) -> TestCaseVersion:
    """Create a new test case version."""
    # Check if test case exists
    test_case = db.query(TestCase).filter(TestCase.id == version_in.test_case_id).first()
    if not test_case:
        raise ValueError(f"Test case with ID {version_in.test_case_id} does not exist")
    
    # Check if creator exists
    creator = db.query(Tester).filter(Tester.id == version_in.created_by).first()
    if not creator:
        raise ValueError(f"Tester with ID {version_in.created_by} does not exist")
    
    # Get next version number
    version_number = get_next_version_number(db, version_in.test_case_id)
    
    version_data = version_in.dict()
    version_data["version"] = version_number
    
    version = TestCaseVersion(**version_data)
    db.add(version)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            if "test_case_id" in str(e):
                raise ValueError(f"Invalid test_case_id: {version_in.test_case_id}")
            elif "created_by" in str(e):
                raise ValueError(f"Invalid created_by: {version_in.created_by}")
        elif "unique constraint" in str(e).lower():
            raise ValueError(f"Version {version_number} already exists for test case {version_in.test_case_id}")
        else:
            raise ValueError(f"Database error: {e}")
    
    db.refresh(version)
    return version


def update_test_case_version(
    db: Session,
    version_id: int,
    version_in: TestCaseVersionUpdate,
) -> Optional[TestCaseVersion]:
    """Update an existing test case version."""
    version = get_test_case_version_by_id(db, version_id)
    if not version:
        return None

    update_data = version_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(version, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Database error: {e}")
    
    db.refresh(version)
    return version


def get_versions_by_test_case(db: Session, test_case_id: int) -> List[TestCaseVersion]:
    """Get all versions for a specific test case."""
    return db.query(TestCaseVersion).filter(
        TestCaseVersion.test_case_id == test_case_id
    ).order_by(desc(TestCaseVersion.version)).all()


def get_version_by_test_case_and_number(db: Session, test_case_id: int, version_number: int) -> Optional[TestCaseVersion]:
    """Get a specific version by test case ID and version number."""
    return db.query(TestCaseVersion).filter(
        and_(
            TestCaseVersion.test_case_id == test_case_id,
            TestCaseVersion.version == version_number
        )
    ).first()


def get_latest_release_ready_version(db: Session, test_case_id: int) -> Optional[TestCaseVersion]:
    """Get the latest release-ready version for a test case."""
    return db.query(TestCaseVersion).filter(
        and_(
            TestCaseVersion.test_case_id == test_case_id,
            TestCaseVersion.release_ready == True
        )
    ).order_by(desc(TestCaseVersion.version)).first()


def create_new_version_from_latest(
    db: Session,
    test_case_id: int,
    created_by: int,
    update_data: Optional[TestCaseVersionUpdate] = None
) -> TestCaseVersion:
    """Create a new version based on the latest version."""
    latest_version = get_latest_version_for_test_case(db, test_case_id)
    
    if not latest_version:
        raise ValueError(f"No existing versions found for test case {test_case_id}")
    
    # Create new version with data from latest version
    new_version_data = {
        "test_case_id": test_case_id,
        "created_by": created_by,
        "release_ready": latest_version.release_ready,
        "name": latest_version.name,
        "description": latest_version.description,
        "steps": latest_version.steps,
        "expected_result": latest_version.expected_result,
    }
    
    # Apply updates if provided
    if update_data:
        update_dict = update_data.dict(exclude_unset=True)
        new_version_data.update(update_dict)
    
    # Get next version number
    version_number = get_next_version_number(db, test_case_id)
    new_version_data["version"] = version_number
    
    version = TestCaseVersion(**new_version_data)
    db.add(version)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Database error: {e}")
    
    db.refresh(version)
    return version