# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/api/v1/test_case.py ---
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.test_case import (
    TestCaseCreate, 
    TestCaseUpdate, 
    TestCaseResponse,
    TestCaseWithRelationsResponse
)
from app.schemas.suitcase import TestCaseWithTestSuitesResponse

from app.services.suitcase import get_test_case_with_test_suites
from app.services.test_case import (
    get_test_cases,
    get_test_case_by_id,
    create_test_case,
    update_test_case,
    get_test_cases_by_scenario,
    get_test_cases_by_status_set,
    get_test_case_with_versions
)

router = APIRouter(prefix="/test_cases", tags=["test_cases"])


@router.get("/", response_model=List[TestCaseResponse])
def read_test_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    scenario_id: int | None = None,
    status_set_id: int | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all test cases with optional filtering."""
    return get_test_cases(
        db=db,
        skip=skip,
        limit=limit,
        scenario_id=scenario_id,
        status_set_id=status_set_id,
    )


@router.get("/{test_case_id}", response_model=TestCaseWithRelationsResponse)
def read_test_case(
    test_case_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get a specific test case by ID."""
    test_case = get_test_case_by_id(db, test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    return test_case


@router.get("/scenario/{scenario_id}", response_model=List[TestCaseResponse])
def read_test_cases_by_scenario(
    scenario_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all test cases for a specific scenario."""
    test_cases = get_test_cases_by_scenario(db, scenario_id)
    return test_cases[skip:skip + limit]


@router.get("/status_set/{status_set_id}", response_model=List[TestCaseResponse])
def read_test_cases_by_status_set(
    status_set_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all test cases for a specific status set."""
    test_cases = get_test_cases_by_status_set(db, status_set_id)
    return test_cases[skip:skip + limit]


@router.post("/", response_model=TestCaseResponse, status_code=status.HTTP_201_CREATED)
def create_new_test_case(
    test_case_data: TestCaseCreate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Create a new test case."""
    try:
        return create_test_case(db, test_case_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{test_case_id}", response_model=TestCaseResponse)
def update_existing_test_case(
    test_case_id: int,
    test_case_data: TestCaseUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Update an existing test case."""
    try:
        updated = update_test_case(db, test_case_id, test_case_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Test case not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{test_case_id}/with-versions", response_model=TestCaseWithRelationsResponse)
def read_test_case_with_versions(
    test_case_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get a test case with its versions (returns basic info, versions would be in a separate endpoint)."""
    test_case = get_test_case_with_versions(db, test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    return test_case


@router.get("/{test_case_id}/test_suites", response_model=TestCaseWithTestSuitesResponse)
def read_test_suites_for_test_case(
    test_case_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all test suites that contain this test case."""
    try:
        return get_test_case_with_test_suites(db, test_case_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))