# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/services/run.py ---
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, func, case
from sqlalchemy.sql import label

from app.database.models import Run, Project, Execution, Status
from app.schemas.run import RunCreate, RunUpdate, RunStatsResponse


def get_run_by_id(db: Session, run_id: int) -> Optional[Run]:
    """Get a single run by ID."""
    return db.query(Run).filter(Run.id == run_id).first()


def get_runs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    project_id: Optional[int] = None,
    started_after: Optional[datetime] = None,
    started_before: Optional[datetime] = None,
    done_after: Optional[datetime] = None,
    done_before: Optional[datetime] = None,
    completed: Optional[bool] = None,
) -> List[Run]:
    """Get multiple runs with optional filtering."""
    query = db.query(Run)

    if name:
        query = query.filter(Run.name.ilike(f"%{name}%"))
    if project_id is not None:
        query = query.filter(Run.project_id == project_id)
    if started_after:
        query = query.filter(Run.started_at >= started_after)
    if started_before:
        query = query.filter(Run.started_at <= started_before)
    if done_after:
        query = query.filter(Run.done_at >= done_after)
    if done_before:
        query = query.filter(Run.done_at <= done_before)
    if completed is not None:
        if completed:
            query = query.filter(Run.done_at.isnot(None))
        else:
            query = query.filter(Run.done_at.is_(None))

    return query.order_by(Run.started_at.desc()).offset(skip).limit(limit).all()


def create_run(db: Session, run_in: RunCreate) -> Run:
    """Create a new run."""
    # Check if project exists
    project = db.query(Project).filter(Project.id == run_in.project_id).first()
    if not project:
        raise ValueError(f"Project with ID {run_in.project_id} does not exist")
    
    run = Run(**run_in.dict())
    db.add(run)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise ValueError(f"Invalid project_id: {run_in.project_id}")
        else:
            raise ValueError(f"Database error: {e}")
    
    db.refresh(run)
    return run


def update_run(
    db: Session,
    run_id: int,
    run_in: RunUpdate,
) -> Optional[Run]:
    """Update an existing run."""
    run = get_run_by_id(db, run_id)
    if not run:
        return None

    update_data = run_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(run, field, value)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise ValueError(f"Invalid project_id in update data")
        else:
            raise ValueError(f"Database error: {e}")
    
    db.refresh(run)
    return run


def get_runs_by_project(db: Session, project_id: int) -> List[Run]:
    """Get all runs for a specific project."""
    return db.query(Run).filter(Run.project_id == project_id).order_by(Run.started_at.desc()).all()


def get_run_stats(db: Session, run_id: int) -> Optional[RunStatsResponse]:
    """Get statistics for a run."""
    run = get_run_by_id(db, run_id)
    if not run:
        return None
    
    # Get execution counts by status
    executions_query = db.query(
        Execution.status_id,
        Status.name,
        func.count(Execution.id).label('count')
    ).join(Status, Execution.status_id == Status.id
    ).filter(Execution.run_id == run_id
    ).group_by(Execution.status_id, Status.name)
    
    executions = executions_query.all()
    
    # Calculate totals
    total_executions = sum(exec.count for exec in executions)
    
    # Map status names to counts
    status_counts = {exec.name: exec.count for exec in executions}
    
    # Calculate duration if run is complete
    duration_seconds = None
    if run.started_at and run.done_at:
        duration_seconds = (run.done_at - run.started_at).total_seconds()
    
    return RunStatsResponse(
        run_id=run.id,
        run_name=run.name,
        total_executions=total_executions,
        completed_executions=total_executions - status_counts.get('Not Run', 0) - status_counts.get('In Progress', 0),
        passed_executions=status_counts.get('Pass', 0),
        failed_executions=status_counts.get('Fail', 0),
        in_progress_executions=status_counts.get('In Progress', 0),
        not_run_executions=status_counts.get('Not Run', 0),
        start_time=run.started_at,
        end_time=run.done_at,
        duration_seconds=duration_seconds
    )


def start_run(db: Session, run_id: int) -> Optional[Run]:
    """Mark a run as started."""
    run = get_run_by_id(db, run_id)
    if not run:
        return None
    
    if not run.started_at:
        run.started_at = datetime.utcnow()
    
    db.commit()
    db.refresh(run)
    return run


def complete_run(db: Session, run_id: int) -> Optional[Run]:
    """Mark a run as completed."""
    run = get_run_by_id(db, run_id)
    if not run:
        return None
    
    run.done_at = datetime.utcnow()
    
    db.commit()
    db.refresh(run)
    return run


def get_active_runs(db: Session) -> List[Run]:
    """Get all active runs (started but not completed)."""
    return db.query(Run).filter(
        and_(
            Run.started_at.isnot(None),
            Run.done_at.is_(None)
        )
    ).order_by(Run.started_at.desc()).all()