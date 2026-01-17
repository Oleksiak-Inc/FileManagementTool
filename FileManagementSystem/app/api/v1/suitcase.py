# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/api/v1/suitcase.py ---
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.suitcase import (
    SuitcaseCreate,
    SuitcaseResponse,
    TestSuiteWithTestCasesResponse,
    TestCaseWithTestSuitesResponse,
    AddTestCaseToSuiteRequest,
    AddTestSuiteToCaseRequest,
    BulkAddTestCasesRequest,
    BulkAddTestSuitesRequest
)
from app.services.suitcase import (
    get_suitcases,
    get_suitcase_by_id,
    create_suitcase,
    get_test_cases_by_test_suite,
    get_test_suites_by_test_case,
    get_test_suite_with_test_cases,
    get_test_case_with_test_suites,
    add_test_case_to_test_suite,
    add_multiple_test_cases_to_test_suite,
    add_test_case_to_multiple_suites
)

router = APIRouter(prefix="/suitcases", tags=["suitcases"])


@router.get("/", response_model=List[SuitcaseResponse])
def read_suitcases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    test_case_id: int | None = None,
    test_suite_id: int | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all suitcases (test case - test suite relationships) with optional filtering."""
    return get_suitcases(
        db=db,
        skip=skip,
        limit=limit,
        test_case_id=test_case_id,
        test_suite_id=test_suite_id,
    )


@router.get("/test_suite/{test_suite_id}/test_cases", response_model=TestSuiteWithTestCasesResponse)
def read_test_cases_in_test_suite(
    test_suite_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all test cases in a specific test suite with their latest versions."""
    try:
        return get_test_suite_with_test_cases(db, test_suite_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/test_case/{test_case_id}/test_suites", response_model=TestCaseWithTestSuitesResponse)
def read_test_suites_for_test_case(
    test_case_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all test suites that contain a specific test case."""
    try:
        return get_test_case_with_test_suites(db, test_case_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=SuitcaseResponse, status_code=status.HTTP_201_CREATED)
def create_new_suitcase(
    suitcase: SuitcaseCreate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Create a new suitcase (link a test case to a test suite)."""
    try:
        return create_suitcase(db, suitcase)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test_suite/{test_suite_id}/test_cases", response_model=List[SuitcaseResponse], status_code=status.HTTP_201_CREATED)
def add_test_case_to_suite(
    test_suite_id: int,
    request: AddTestCaseToSuiteRequest,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Add a test case to a test suite."""
    try:
        suitcase = add_test_case_to_test_suite(db, request.test_case_id, test_suite_id)
        return [suitcase]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test_suite/{test_suite_id}/test_cases/bulk", response_model=List[SuitcaseResponse], status_code=status.HTTP_201_CREATED)
def add_multiple_test_cases_to_suite(
    test_suite_id: int,
    request: BulkAddTestCasesRequest,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Add multiple test cases to a test suite."""
    try:
        return add_multiple_test_cases_to_test_suite(db, request.test_case_ids, test_suite_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test_case/{test_case_id}/test_suites", response_model=List[SuitcaseResponse], status_code=status.HTTP_201_CREATED)
def add_test_suite_to_case(
    test_case_id: int,
    request: AddTestSuiteToCaseRequest,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Add a test case to a test suite."""
    try:
        suitcase = add_test_case_to_test_suite(db, test_case_id, request.test_suite_id)
        return [suitcase]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test_case/{test_case_id}/test_suites/bulk", response_model=List[SuitcaseResponse], status_code=status.HTTP_201_CREATED)
def add_case_to_multiple_suites(
    test_case_id: int,
    request: BulkAddTestSuitesRequest,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Add a test case to multiple test suites."""
    try:
        return add_test_case_to_multiple_suites(db, test_case_id, request.test_suite_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
