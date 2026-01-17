# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/api/v1/run.py ---
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import get_db
from app.api.dependencies import get_current_tester
from app.database.models import Tester as TesterModel
from app.schemas.run import (
    RunCreate,
    RunUpdate,
    RunResponse,
    RunWithRelationsResponse,
    RunStatsResponse
)
from app.services.run import (
    get_runs,
    get_run_by_id,
    create_run,
    update_run,
    get_runs_by_project,
    get_run_stats,
    start_run,
    complete_run,
    get_active_runs
)

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("/", response_model=List[RunResponse])
def read_runs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    name: str | None = None,
    project_id: int | None = None,
    started_after: datetime | None = None,
    started_before: datetime | None = None,
    done_after: datetime | None = None,
    done_before: datetime | None = None,
    completed: bool | None = None,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all runs with optional filtering."""
    return get_runs(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        project_id=project_id,
        started_after=started_after,
        started_before=started_before,
        done_after=done_after,
        done_before=done_before,
        completed=completed,
    )


@router.get("/{run_id}", response_model=RunWithRelationsResponse)
def read_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get a specific run by ID."""
    run = get_run_by_id(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.get("/project/{project_id}", response_model=List[RunResponse])
def read_runs_by_project(
    project_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all runs for a specific project."""
    runs = get_runs_by_project(db, project_id)
    return runs[skip:skip + limit]


@router.get("/{run_id}/stats", response_model=RunStatsResponse)
def read_run_stats(
    run_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get statistics for a run."""
    stats = get_run_stats(db, run_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Run not found")
    return stats


@router.get("/active/list", response_model=List[RunResponse])
def read_active_runs(
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Get all active runs (started but not completed)."""
    return get_active_runs(db)


@router.post("/", response_model=RunResponse, status_code=status.HTTP_201_CREATED)
def create_new_run(
    run_data: RunCreate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Create a new run."""
    try:
        return create_run(db, run_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{run_id}/start", response_model=RunResponse)
def start_existing_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Mark a run as started."""
    run = start_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.post("/{run_id}/complete", response_model=RunResponse)
def complete_existing_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Mark a run as completed."""
    run = complete_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.patch("/{run_id}", response_model=RunResponse)
def update_existing_run(
    run_id: int,
    run_data: RunUpdate,
    db: Session = Depends(get_db),
    current_tester: TesterModel = Depends(get_current_tester),
):
    """Update an existing run."""
    try:
        updated = update_run(db, run_id, run_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Run not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Remove the start-with-executions endpoint as execution initialization
# should only happen via Execution API