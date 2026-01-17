# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/schemas/run.py ---
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class RunBase(BaseModel):
    name: str
    project_id: int
    test_suite_metadata: Optional[str] = None
    started_at: Optional[datetime] = None
    done_at: Optional[datetime] = None


class RunCreate(RunBase):
    pass


class RunUpdate(BaseModel):
    name: Optional[str] = None
    project_id: Optional[int] = None
    test_suite_metadata: Optional[str] = None
    started_at: Optional[datetime] = None
    done_at: Optional[datetime] = None


class RunResponse(RunBase):
    id: int

    class Config:
        from_attributes = True


class RunWithRelationsResponse(RunResponse):
    project: Optional[dict] = None
    executions: Optional[List[dict]] = None
    
    class Config:
        from_attributes = True


class RunStatsResponse(BaseModel):
    run_id: int
    run_name: str
    total_executions: int
    completed_executions: int
    passed_executions: int
    failed_executions: int
    in_progress_executions: int
    not_run_executions: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None


class RunFilter(BaseModel):
    name: Optional[str] = None
    project_id: Optional[int] = None
    started_after: Optional[datetime] = None
    started_before: Optional[datetime] = None
    done_after: Optional[datetime] = None
    done_before: Optional[datetime] = None
    completed: Optional[bool] = None  # True if done_at is set, False if done_at is None