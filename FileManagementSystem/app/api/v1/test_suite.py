from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester
from app.schemas.test_suite import TestSuiteCreate, TestSuiteUpdate, TestSuiteResponse
from app.schemas.suitcase import TestSuiteWithTestCasesResponse
from app.services.suitcase import get_test_suite_with_test_cases
from app.services.test_suite import (
    get_test_suites, get_test_suite_by_id, create_test_suite, update_test_suite
)

router = APIRouter(prefix="/test_suites", tags=["test_suites"])


@router.get("/", response_model=List[TestSuiteResponse])
def read_test_suites(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    return get_test_suites(db, skip, limit)


@router.get("/{test_suite_id}", response_model=TestSuiteResponse)
def read_test_suite(
    test_suite_id: int,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    test_suite = get_test_suite_by_id(db, test_suite_id)
    if not test_suite:
        raise HTTPException(status_code=404, detail="TestSuite not found")
    return test_suite


@router.post("/", response_model=TestSuiteResponse, status_code=status.HTTP_201_CREATED)
def create_new_test_suite(
    test_suite: TestSuiteCreate,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    return create_test_suite(db, test_suite)


@router.patch("/{test_suite_id}", response_model=TestSuiteResponse)
def update_existing_test_suite(
    test_suite_id: int,
    test_suite: TestSuiteUpdate,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    updated = update_test_suite(db, test_suite_id, test_suite)
    if not updated:
        raise HTTPException(status_code=404, detail="TestSuite not found")
    return updated


@router.get("/{test_suite_id}/test_cases", response_model=TestSuiteWithTestCasesResponse)
def read_test_cases_in_test_suite(
    test_suite_id: int,
    db: Session = Depends(get_db),
    _: Tester = Depends(get_current_tester),
):
    """Get all test cases in this test suite with their latest versions."""
    try:
        return get_test_suite_with_test_cases(db, test_suite_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))