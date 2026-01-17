from typing import List, Optional
from sqlalchemy.orm import Session

from app.database.models import TestSuite
from app.schemas.test_suite import TestSuiteCreate, TestSuiteUpdate


def get_test_suite_by_id(db: Session, test_suite_id: int) -> Optional[TestSuite]:
    return db.query(TestSuite).filter(TestSuite.id == test_suite_id).first()


def get_test_suites(db: Session, skip: int = 0, limit: int = 100) -> List[TestSuite]:
    return db.query(TestSuite).offset(skip).limit(limit).all()


def create_test_suite(db: Session, test_suite_in: TestSuiteCreate) -> TestSuite:
    test_suite = TestSuite(**test_suite_in.dict())
    db.add(test_suite)
    db.commit()
    db.refresh(test_suite)
    return test_suite


def update_test_suite(db: Session, test_suite_id: int, test_suite_in: TestSuiteUpdate) -> Optional[TestSuite]:
    test_suite = get_test_suite_by_id(db, test_suite_id)
    if not test_suite:
        return None

    for field, value in test_suite_in.dict(exclude_unset=True).items():
        setattr(test_suite, field, value)

    db.commit()
    db.refresh(test_suite)
    return test_suite
