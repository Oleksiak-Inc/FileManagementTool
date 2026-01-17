# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/schemas/execution.py ---
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class ExecutionBase(BaseModel):
    device_id: int
    run_id: int
    test_case_version_id: int
    executed_by: int
    status_id: int
    attachment_id: Optional[int] = None
    actual_result: Optional[str] = None
    executed_at: Optional[datetime] = None
    execution_order: int


class ExecutionCreate(ExecutionBase):
    pass


class ExecutionUpdate(BaseModel):
    device_id: Optional[int] = None
    run_id: Optional[int] = None
    test_case_version_id: Optional[int] = None
    executed_by: Optional[int] = None
    status_id: Optional[int] = None
    attachment_id: Optional[int] = None
    actual_result: Optional[str] = None
    executed_at: Optional[datetime] = None
    execution_order: Optional[int] = None


class ExecutionResponse(ExecutionBase):
    id: int
    
    class Config:
        from_attributes = True


class ExecutionWithRelationsResponse(ExecutionResponse):
    device: Optional[Dict[str, Any]] = None
    run: Optional[Dict[str, Any]] = None
    test_case_version: Optional[Dict[str, Any]] = None
    executor: Optional[Dict[str, Any]] = None
    status: Optional[Dict[str, Any]] = None
    attachment: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


class ExecutionStatsResponse(BaseModel):
    total_executions: int
    passed_executions: int
    failed_executions: int
    in_progress_executions: int
    blocked_executions: int
    not_run_executions: int
    completed_executions: int
    average_execution_time_seconds: Optional[float] = None


class ExecutionFilter(BaseModel):
    device_id: Optional[int] = None
    run_id: Optional[int] = None
    test_case_version_id: Optional[int] = None
    executed_by: Optional[int] = None
    status_id: Optional[int] = None
    attachment_id: Optional[int] = None
    executed_after: Optional[datetime] = None
    executed_before: Optional[datetime] = None
    project_id: Optional[int] = None
    test_case_id: Optional[int] = None
    test_suite_id: Optional[int] = None
    scenario_id: Optional[int] = None


class ExecutionStatusUpdate(BaseModel):
    status_id: int
    actual_result: Optional[str] = None
    attachment_id: Optional[int] = None


class ExecutionSummaryResponse(BaseModel):
    execution_id: int
    test_case_name: Optional[str] = None
    test_case_version: int
    status_name: str
    executed_by: str
    device_name: str
    run_name: str
    executed_at: Optional[datetime] = None
    execution_order: int


# Schema for creating executions automatically from a test suite
class RunWithExecutionsCreate(BaseModel):
    name: str
    project_id: int
    test_suite_id: int
    test_suite_metadata: Optional[str] = None
    started_at: Optional[datetime] = None
    done_at: Optional[datetime] = None