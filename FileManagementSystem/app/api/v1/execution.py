# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/api/v1/execution.py ---
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.execution import (
    ExecutionCreate,
    ExecutionUpdate,
    ExecutionResponse,
    ExecutionWithRelationsResponse,
    ExecutionStatsResponse,
    ExecutionFilter,
    ExecutionSummaryResponse,
    ExecutionStatusUpdate
)
from app.services.execution import (
    get_executions,
    get_execution_by_id,
    create_execution,
    update_execution,
    get_executions_by_run,
    get_executions_by_device,
    get_executions_by_tester,
    get_executions_by_test_case,
    get_executions_by_test_suite,
    get_execution_stats,
    get_execution_with_relations,
    update_execution_status,
    create_executions_for_test_suite,
    reassign_execution_device,
    reassign_execution_tester
)

router = APIRouter(prefix="/executions", tags=["executions"])


class BulkCreateExecutionsRequest(BaseModel):
    """Request model for bulk execution creation from test suite."""
    run_id: int
    test_suite_id: int
    device_id: int
    version_override: dict = {}  # Optional mapping of test_case_id -> test_case_version_id


@router.get("/", response_model=List[ExecutionResponse])
def read_executions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    device_id: int | None = None,
    run_id: int | None = None,
    test_case_version_id: int | None = None,
    executed_by: int | None = None,
    status_id: int | None = None,
    attachment_id: int | None = None,
    executed_after: datetime | None = None,
    executed_before: datetime | None = None,
    project_id: int | None = None,
    test_case_id: int | None = None,
    test_suite_id: int | None = None,
    scenario_id: int | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all executions with optional filtering."""
    return get_executions(
        db=db,
        skip=skip,
        limit=limit,
        device_id=device_id,
        run_id=run_id,
        test_case_version_id=test_case_version_id,
        executed_by=executed_by,
        status_id=status_id,
        attachment_id=attachment_id,
        executed_after=executed_after,
        executed_before=executed_before,
        project_id=project_id,
        test_case_id=test_case_id,
        test_suite_id=test_suite_id,
        scenario_id=scenario_id,
    )


@router.get("/{execution_id}", response_model=ExecutionWithRelationsResponse)
def read_execution(
    execution_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get a specific execution by ID with all relations."""
    execution = get_execution_with_relations(db, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution


@router.get("/run/{run_id}/list", response_model=List[ExecutionResponse])
def read_executions_by_run(
    run_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all executions for a specific run."""
    executions = get_executions_by_run(db, run_id)
    return executions[skip:skip + limit]


@router.get("/device/{device_id}/list", response_model=List[ExecutionResponse])
def read_executions_by_device(
    device_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all executions on a specific device."""
    executions = get_executions_by_device(db, device_id)
    return executions[skip:skip + limit]


@router.get("/tester/{tester_id}/list", response_model=List[ExecutionResponse])
def read_executions_by_tester(
    tester_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all executions performed by a specific tester."""
    executions = get_executions_by_tester(db, tester_id)
    return executions[skip:skip + limit]


@router.get("/test_case/{test_case_id}/list", response_model=List[ExecutionResponse])
def read_executions_by_test_case(
    test_case_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all executions for a specific test case (across all versions)."""
    executions = get_executions_by_test_case(db, test_case_id)
    return executions[skip:skip + limit]


@router.get("/test_suite/{test_suite_id}/list", response_model=List[ExecutionResponse])
def read_executions_by_test_suite(
    test_suite_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all executions for test cases in a specific test suite."""
    executions = get_executions_by_test_suite(db, test_suite_id)
    return executions[skip:skip + limit]


@router.get("/stats/summary", response_model=ExecutionStatsResponse)
def read_execution_stats(
    run_id: int | None = None,
    project_id: int | None = None,
    device_id: int | None = None,
    executed_by: int | None = None,
    executed_after: datetime | None = None,
    executed_before: datetime | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get execution statistics."""
    filters = {}
    if run_id is not None:
        filters["run_id"] = run_id
    if project_id is not None:
        filters["project_id"] = project_id
    if device_id is not None:
        filters["device_id"] = device_id
    if executed_by is not None:
        filters["executed_by"] = executed_by
    if executed_after is not None:
        filters["executed_after"] = executed_after
    if executed_before is not None:
        filters["executed_before"] = executed_before
    
    stats = get_execution_stats(db, filters)
    return ExecutionStatsResponse(**stats)


@router.post("/bulk-create-from-test-suite", response_model=List[ExecutionResponse], status_code=status.HTTP_201_CREATED)
def bulk_create_executions_from_test_suite(
    request: BulkCreateExecutionsRequest,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Create executions in bulk when test cases are assigned to a test suite."""
    try:
        executions = create_executions_for_test_suite(
            db=db,
            run_id=request.run_id,
            test_suite_id=request.test_suite_id,
            device_id=request.device_id,
            executed_by=current_tester.id,
            version_override=request.version_override
        )
        return executions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=ExecutionResponse, status_code=status.HTTP_201_CREATED)
def create_new_execution(
    execution_data: ExecutionCreate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Create a new execution (manual creation)."""
    try:
        return create_execution(db, execution_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{execution_id}", response_model=ExecutionResponse)
def update_existing_execution(
    execution_id: int,
    execution_data: ExecutionUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Update an existing execution."""
    execution = get_execution_by_id(db, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    # Check permissions - only executor or admin can update
    if execution.executed_by != current_tester.id and current_tester.tester_type_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="Not authorized to update this execution")
    
    try:
        updated = update_execution(db, execution_id, execution_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Execution not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{execution_id}/status", response_model=ExecutionResponse)
def update_execution_status_endpoint(
    execution_id: int,
    status_update: ExecutionStatusUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Update an execution's status, actual result, and/or attachment."""
    execution = get_execution_by_id(db, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    # Check permissions - only assigned tester or admin can update status
    if execution.executed_by != current_tester.id and current_tester.tester_type_id not in [1, 2]:
        raise HTTPException(status_code=403, detail="Not authorized to update this execution's status")
    
    try:
        updated = update_execution_status(
            db,
            execution_id,
            status_update.status_id,
            status_update.actual_result,
            status_update.attachment_id
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Execution not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{execution_id}/reassign-device", response_model=ExecutionResponse)
def reassign_execution_device_endpoint(
    execution_id: int,
    new_device_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Reassign an execution to a different device."""
    execution = get_execution_by_id(db, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    # Check permissions - only admin or project manager can reassign devices
    if current_tester.tester_type_id not in [1, 2]:  # Only super/admin
        raise HTTPException(status_code=403, detail="Not authorized to reassign devices")
    
    try:
        updated = reassign_execution_device(db, execution_id, new_device_id)
        if not updated:
            raise HTTPException(status_code=404, detail="Execution not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{execution_id}/reassign-tester", response_model=ExecutionResponse)
def reassign_execution_tester_endpoint(
    execution_id: int,
    new_tester_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Reassign an execution to a different tester."""
    execution = get_execution_by_id(db, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    # Check permissions - only admin or project manager can reassign testers
    if current_tester.tester_type_id not in [1, 2]:  # Only super/admin
        raise HTTPException(status_code=403, detail="Not authorized to reassign testers")
    
    try:
        updated = reassign_execution_tester(db, execution_id, new_tester_id)
        if not updated:
            raise HTTPException(status_code=404, detail="Execution not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/run/{run_id}/summary", response_model=List[ExecutionSummaryResponse])
def read_run_execution_summary(
    run_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get a summary of all executions in a run with relevant information."""
    from sqlalchemy.orm import aliased
    
    # Create aliases for joins
    DeviceAlias = aliased(Device)
    RunAlias = aliased(Run)
    TestCaseVersionAlias = aliased(TestCaseVersion)
    TestCaseAlias = aliased(TestCase)
    TesterAlias = aliased(Tester)
    StatusAlias = aliased(Status)
    
    results = db.query(
        Execution.id.label("execution_id"),
        TestCaseVersionAlias.name.label("test_case_name"),
        TestCaseVersionAlias.version.label("test_case_version"),
        StatusAlias.name.label("status_name"),
        func.concat(TesterAlias.first_name, ' ', TesterAlias.last_name).label("executed_by"),
        DeviceAlias.name_external.label("device_name"),
        RunAlias.name.label("run_name"),
        Execution.executed_at,
        Execution.execution_order
    ).join(DeviceAlias, Execution.device_id == DeviceAlias.id
    ).join(RunAlias, Execution.run_id == RunAlias.id
    ).join(TestCaseVersionAlias, Execution.test_case_version_id == TestCaseVersionAlias.id
    ).join(TestCaseAlias, TestCaseVersionAlias.test_case_id == TestCaseAlias.id
    ).join(TesterAlias, Execution.executed_by == TesterAlias.id
    ).join(StatusAlias, Execution.status_id == StatusAlias.id
    ).filter(Execution.run_id == run_id
    ).order_by(Execution.execution_order.asc()
    ).all()
    
    return [
        ExecutionSummaryResponse(
            execution_id=result.execution_id,
            test_case_name=result.test_case_name,
            test_case_version=result.test_case_version,
            status_name=result.status_name,
            executed_by=result.executed_by,
            device_name=result.device_name,
            run_name=result.run_name,
            executed_at=result.executed_at,
            execution_order=result.execution_order
        )
        for result in results
    ]