# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/api/v1/test_case_version.py ---
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.test_case_version import (
    TestCaseVersionCreate,
    TestCaseVersionUpdate,
    TestCaseVersionResponse,
    TestCaseVersionWithRelationsResponse,
    TestCaseVersionCreateResponse,
)
from app.services.test_case_version import (
    get_test_case_versions,
    get_test_case_version_by_id,
    create_test_case_version,
    update_test_case_version,
    get_versions_by_test_case,
    get_version_by_test_case_and_number,
    get_latest_version_for_test_case,
    get_latest_release_ready_version,
    create_new_version_from_latest,
)

router = APIRouter(prefix="/test_case_versions", tags=["test_case_versions"])


@router.get("/", response_model=List[TestCaseVersionResponse])
def read_test_case_versions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    test_case_id: int | None = None,
    created_by: int | None = None,
    release_ready: bool | None = None,
    version: int | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all test case versions with optional filtering."""
    return get_test_case_versions(
        db=db,
        skip=skip,
        limit=limit,
        test_case_id=test_case_id,
        created_by=created_by,
        release_ready=release_ready,
        version=version,
    )


@router.get("/{version_id}", response_model=TestCaseVersionWithRelationsResponse)
def read_test_case_version(
    version_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get a specific test case version by ID."""
    version = get_test_case_version_by_id(db, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Test case version not found")
    return version


@router.get("/test_case/{test_case_id}", response_model=List[TestCaseVersionResponse])
def read_versions_by_test_case(
    test_case_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all versions for a specific test case."""
    versions = get_versions_by_test_case(db, test_case_id)
    return versions[skip:skip + limit]


@router.get("/test_case/{test_case_id}/latest", response_model=TestCaseVersionWithRelationsResponse)
def read_latest_version_for_test_case(
    test_case_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get the latest version for a test case."""
    version = get_latest_version_for_test_case(db, test_case_id)
    if not version:
        raise HTTPException(status_code=404, detail="No versions found for this test case")
    return version


@router.get("/test_case/{test_case_id}/latest/release-ready", response_model=TestCaseVersionWithRelationsResponse)
def read_latest_release_ready_version(
    test_case_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get the latest release-ready version for a test case."""
    version = get_latest_release_ready_version(db, test_case_id)
    if not version:
        raise HTTPException(status_code=404, detail="No release-ready versions found for this test case")
    return version


@router.get("/test_case/{test_case_id}/version/{version_number}", response_model=TestCaseVersionWithRelationsResponse)
def read_version_by_test_case_and_number(
    test_case_id: int,
    version_number: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get a specific version by test case ID and version number."""
    version = get_version_by_test_case_and_number(db, test_case_id, version_number)
    if not version:
        raise HTTPException(status_code=404, detail="Test case version not found")
    return version


@router.post("/", response_model=TestCaseVersionCreateResponse, status_code=status.HTTP_201_CREATED)
def create_new_test_case_version(
    version_data: TestCaseVersionCreate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Create a new test case version."""
    # Ensure the creator is the current tester (or an admin can create for others)
    if version_data.created_by != current_tester.id and current_tester.tester_type_id not in [1, 2]:  # Only super/admin can create for others
        raise HTTPException(status_code=403, detail="Not authorized to create versions for other testers")
    
    try:
        return create_test_case_version(db, version_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/test_case/{test_case_id}/new-from-latest", response_model=TestCaseVersionCreateResponse, status_code=status.HTTP_201_CREATED)
def create_new_version_from_latest(
    test_case_id: int,
    update_data: TestCaseVersionUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Create a new version based on the latest version."""
    try:
        new_version = create_new_version_from_latest(
            db, test_case_id, current_tester.id, update_data
        )
        return new_version
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{version_id}", response_model=TestCaseVersionResponse)
def update_existing_test_case_version(
    version_id: int,
    version_data: TestCaseVersionUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Update an existing test case version."""
    version = get_test_case_version_by_id(db, version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Test case version not found")
    
    # Check permissions - only creator or admin can update
    if version.created_by != current_tester.id and current_tester.tester_type_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="Not authorized to update this version")
    
    try:
        updated = update_test_case_version(db, version_id, version_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Test case version not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

