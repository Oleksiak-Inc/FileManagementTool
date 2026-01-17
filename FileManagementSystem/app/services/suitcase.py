# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/services/suitcase.py ---
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.models import Suitcase, TestCase, TestSuite, TestCaseVersion
from app.schemas.suitcase import SuitcaseCreate


def get_suitcase_by_id(db: Session, suitcase_id: int) -> Optional[Suitcase]:
    """Get a single suitcase by ID."""
    return db.query(Suitcase).filter(Suitcase.id == suitcase_id).first()


def get_suitcases(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    test_case_id: Optional[int] = None,
    test_suite_id: Optional[int] = None,
) -> List[Suitcase]:
    """Get multiple suitcases with optional filtering."""
    query = db.query(Suitcase)

    if test_case_id is not None:
        query = query.filter(Suitcase.test_case_id == test_case_id)
    if test_suite_id is not None:
        query = query.filter(Suitcase.test_suite_id == test_suite_id)

    return query.offset(skip).limit(limit).all()


def create_suitcase(db: Session, suitcase_in: SuitcaseCreate) -> Suitcase:
    """Create a new suitcase (link between test case and test suite)."""
    # Check if test case exists
    test_case = db.query(TestCase).filter(TestCase.id == suitcase_in.test_case_id).first()
    if not test_case:
        raise ValueError(f"Test case with ID {suitcase_in.test_case_id} does not exist")
    
    # Check if test suite exists
    test_suite = db.query(TestSuite).filter(TestSuite.id == suitcase_in.test_suite_id).first()
    if not test_suite:
        raise ValueError(f"Test suite with ID {suitcase_in.test_suite_id} does not exist")
    
    # Check if the relationship already exists
    existing = db.query(Suitcase).filter(
        Suitcase.test_case_id == suitcase_in.test_case_id,
        Suitcase.test_suite_id == suitcase_in.test_suite_id
    ).first()
    
    if existing:
        raise ValueError(f"Test case {suitcase_in.test_case_id} is already in test suite {suitcase_in.test_suite_id}")
    
    suitcase = Suitcase(**suitcase_in.dict())
    db.add(suitcase)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Database error: {e}")
    
    db.refresh(suitcase)
    return suitcase


def get_test_cases_by_test_suite(db: Session, test_suite_id: int) -> List[TestCase]:
    """Get all test cases for a specific test suite."""
    return db.query(TestCase).join(Suitcase).filter(Suitcase.test_suite_id == test_suite_id).all()


def get_test_suites_by_test_case(db: Session, test_case_id: int) -> List[TestSuite]:
    """Get all test suites for a specific test case."""
    return db.query(TestSuite).join(Suitcase).filter(Suitcase.test_case_id == test_case_id).all()


def get_test_suite_with_test_cases(db: Session, test_suite_id: int) -> Dict[str, Any]:
    """Get a test suite with all its test cases and their latest versions."""
    test_suite = db.query(TestSuite).filter(TestSuite.id == test_suite_id).first()
    if not test_suite:
        raise ValueError(f"Test suite with ID {test_suite_id} does not exist")
    
    # Get test cases with their latest versions
    test_cases = db.query(
        TestCase,
        TestCaseVersion
    ).join(Suitcase, TestCase.id == Suitcase.test_case_id
    ).outerjoin(
        TestCaseVersion,
        (TestCaseVersion.test_case_id == TestCase.id) &
        (TestCaseVersion.version == db.query(
            TestCaseVersion.version
        ).filter(
            TestCaseVersion.test_case_id == TestCase.id
        ).order_by(
            TestCaseVersion.version.desc()
        ).limit(1).as_scalar())
    ).filter(Suitcase.test_suite_id == test_suite_id).all()
    
    # Format the response
    test_cases_list = []
    for test_case, latest_version in test_cases:
        test_case_data = {
            "id": test_case.id,
            "scenario_id": test_case.scenario_id,
            "status_set_id": test_case.status_set_id,
            "created_at": test_case.created_at,
            "latest_version": None
        }
        
        if latest_version:
            test_case_data["latest_version"] = {
                "id": latest_version.id,
                "version": latest_version.version,
                "name": latest_version.name,
                "description": latest_version.description,
                "release_ready": latest_version.release_ready,
                "created_at": latest_version.created_at
            }
        
        test_cases_list.append(test_case_data)
    
    return {
        "test_suite_id": test_suite.id,
        "test_suite_name": test_suite.name,
        "test_cases": test_cases_list
    }


def get_test_case_with_test_suites(db: Session, test_case_id: int) -> Dict[str, Any]:
    """Get a test case with all its test suites."""
    test_case = db.query(TestCase).filter(TestCase.id == test_case_id).first()
    if not test_case:
        raise ValueError(f"Test case with ID {test_case_id} does not exist")
    
    test_suites = get_test_suites_by_test_case(db, test_case_id)
    
    return {
        "test_case_id": test_case.id,
        "test_suites": [
            {
                "id": suite.id,
                "name": suite.name
            }
            for suite in test_suites
        ]
    }


def add_test_case_to_test_suite(db: Session, test_case_id: int, test_suite_id: int) -> Suitcase:
    """Add a test case to a test suite."""
    suitcase_data = SuitcaseCreate(
        test_case_id=test_case_id,
        test_suite_id=test_suite_id
    )
    
    return create_suitcase(db, suitcase_data)


def add_multiple_test_cases_to_test_suite(db: Session, test_case_ids: List[int], test_suite_id: int) -> List[Suitcase]:
    """Add multiple test cases to a test suite."""
    results = []
    
    for test_case_id in test_case_ids:
        try:
            suitcase_data = SuitcaseCreate(
                test_case_id=test_case_id,
                test_suite_id=test_suite_id
            )
            suitcase = create_suitcase(db, suitcase_data)
            results.append(suitcase)
        except ValueError as e:
            # Skip duplicates and continue with others
            continue
    
    return results


def add_test_case_to_multiple_suites(db: Session, test_case_id: int, test_suite_ids: List[int]) -> List[Suitcase]:
    """Add a test case to multiple test suites."""
    results = []
    
    for test_suite_id in test_suite_ids:
        try:
            suitcase_data = SuitcaseCreate(
                test_case_id=test_case_id,
                test_suite_id=test_suite_id
            )
            suitcase = create_suitcase(db, suitcase_data)
            results.append(suitcase)
        except ValueError as e:
            # Skip duplicates and continue with others
            continue
    
    return results