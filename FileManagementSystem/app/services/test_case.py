# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/services/test_case.py ---
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from app.database.models import TestCase
from app.schemas.test_case import TestCaseCreate, TestCaseUpdate


def get_test_case_by_id(db: Session, test_case_id: int) -> Optional[TestCase]:
    """Get a single test case by ID."""
    return db.query(TestCase).filter(TestCase.id == test_case_id).first()


def get_test_cases(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    scenario_id: Optional[int] = None,
    status_set_id: Optional[int] = None,
) -> List[TestCase]:
    """Get multiple test cases with optional filtering."""
    query = db.query(TestCase)

    if scenario_id is not None:
        query = query.filter(TestCase.scenario_id == scenario_id)
    if status_set_id is not None:
        query = query.filter(TestCase.status_set_id == status_set_id)

    return query.offset(skip).limit(limit).all()


def create_test_case(db: Session, test_case_in: TestCaseCreate) -> TestCase:
    """Create a new test case."""
    test_case = TestCase(**test_case_in.dict())
    db.add(test_case)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Check if it's a foreign key violation
        if "foreign key constraint" in str(e).lower():
            if "scenario_id" in str(e):
                raise ValueError(f"Invalid scenario_id: {test_case_in.scenario_id}")
            elif "status_set_id" in str(e):
                raise ValueError(f"Invalid status_set_id: {test_case_in.status_set_id}")
        else:
            raise ValueError(f"Database error: {e}")
    db.refresh(test_case)
    return test_case


def update_test_case(
    db: Session,
    test_case_id: int,
    test_case_in: TestCaseUpdate,
) -> Optional[TestCase]:
    """Update an existing test case."""
    test_case = get_test_case_by_id(db, test_case_id)
    if not test_case:
        return None

    update_data = test_case_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(test_case, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            if "scenario_id" in str(e):
                raise ValueError(f"Invalid scenario_id: {test_case_in.scenario_id}")
            elif "status_set_id" in str(e):
                raise ValueError(f"Invalid status_set_id: {test_case_in.status_set_id}")
        else:
            raise ValueError(f"Database error: {e}")
    
    db.refresh(test_case)
    return test_case


def get_test_cases_by_scenario(db: Session, scenario_id: int) -> List[TestCase]:
    """Get all test cases for a specific scenario."""
    return db.query(TestCase).filter(TestCase.scenario_id == scenario_id).all()


def get_test_cases_by_status_set(db: Session, status_set_id: int) -> List[TestCase]:
    """Get all test cases for a specific status set."""
    return db.query(TestCase).filter(TestCase.status_set_id == status_set_id).all()


def get_test_case_with_versions(db: Session, test_case_id: int) -> Optional[TestCase]:
    """Get a test case with its versions."""
    return db.query(TestCase).filter(TestCase.id == test_case_id).first()