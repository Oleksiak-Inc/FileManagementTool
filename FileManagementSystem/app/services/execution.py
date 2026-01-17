# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/services/execution.py ---
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, func, desc, asc, case
from sqlalchemy.sql import label

from app.database.models import (
    Execution, Device, Run, TestCaseVersion, Tester, 
    Status, Attachment, Project, TestCase, TestSuite,
    Suitcase, Scenario
)
from app.schemas.execution import ExecutionCreate, ExecutionUpdate


def get_execution_by_id(db: Session, execution_id: int) -> Optional[Execution]:
    """Get a single execution by ID."""
    return db.query(Execution).filter(Execution.id == execution_id).first()


def get_executions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    device_id: Optional[int] = None,
    run_id: Optional[int] = None,
    test_case_version_id: Optional[int] = None,
    executed_by: Optional[int] = None,
    status_id: Optional[int] = None,
    attachment_id: Optional[int] = None,
    executed_after: Optional[datetime] = None,
    executed_before: Optional[datetime] = None,
    project_id: Optional[int] = None,
    test_case_id: Optional[int] = None,
    test_suite_id: Optional[int] = None,
    scenario_id: Optional[int] = None,
) -> List[Execution]:
    """Get multiple executions with optional filtering."""
    query = db.query(Execution)
    
    # Join tables for complex filtering
    if any([project_id, test_case_id, test_suite_id, scenario_id]):
        query = query.join(Device).join(Run).join(TestCaseVersion)
    
    # Apply filters
    if device_id is not None:
        query = query.filter(Execution.device_id == device_id)
    if run_id is not None:
        query = query.filter(Execution.run_id == run_id)
    if test_case_version_id is not None:
        query = query.filter(Execution.test_case_version_id == test_case_version_id)
    if executed_by is not None:
        query = query.filter(Execution.executed_by == executed_by)
    if status_id is not None:
        query = query.filter(Execution.status_id == status_id)
    if attachment_id is not None:
        query = query.filter(Execution.attachment_id == attachment_id)
    if executed_after:
        query = query.filter(Execution.executed_at >= executed_after)
    if executed_before:
        query = query.filter(Execution.executed_at <= executed_before)
    
    # Complex filters requiring joins
    if project_id is not None:
        query = query.filter(Device.project_id == project_id)
    if test_case_id is not None:
        query = query.filter(TestCaseVersion.test_case_id == test_case_id)
    if test_suite_id is not None:
        # Get test case IDs from the suitcase table
        subquery = db.query(Suitcase.test_case_id).filter(
            Suitcase.test_suite_id == test_suite_id
        ).subquery()
        query = query.filter(TestCaseVersion.test_case_id.in_(subquery))
    if scenario_id is not None:
        # Get test case IDs with the given scenario
        subquery = db.query(TestCase.id).filter(
            TestCase.scenario_id == scenario_id
        ).subquery()
        query = query.filter(TestCaseVersion.test_case_id.in_(subquery))
    
    return query.order_by(
        desc(Execution.executed_at), 
        asc(Execution.execution_order)
    ).offset(skip).limit(limit).all()


def create_execution(db: Session, execution_in: ExecutionCreate) -> Execution:
    """Create a new execution."""
    # Validate foreign key references
    device = db.query(Device).filter(Device.id == execution_in.device_id).first()
    if not device:
        raise ValueError(f"Device with ID {execution_in.device_id} does not exist")
    
    run = db.query(Run).filter(Run.id == execution_in.run_id).first()
    if not run:
        raise ValueError(f"Run with ID {execution_in.run_id} does not exist")
    
    test_case_version = db.query(TestCaseVersion).filter(
        TestCaseVersion.id == execution_in.test_case_version_id
    ).first()
    if not test_case_version:
        raise ValueError(f"Test case version with ID {execution_in.test_case_version_id} does not exist")
    
    tester = db.query(Tester).filter(Tester.id == execution_in.executed_by).first()
    if not tester:
        raise ValueError(f"Tester with ID {execution_in.executed_by} does not exist")
    
    status = db.query(Status).filter(Status.id == execution_in.status_id).first()
    if not status:
        raise ValueError(f"Status with ID {execution_in.status_id} does not exist")
    
    if execution_in.attachment_id:
        attachment = db.query(Attachment).filter(
            Attachment.id == execution_in.attachment_id
        ).first()
        if not attachment:
            raise ValueError(f"Attachment with ID {execution_in.attachment_id} does not exist")
    
    # Check unique constraint
    existing = db.query(Execution).filter(
        and_(
            Execution.run_id == execution_in.run_id,
            Execution.test_case_version_id == execution_in.test_case_version_id
        )
    ).first()
    
    if existing:
        raise ValueError(f"Execution already exists for run {execution_in.run_id} and test case version {execution_in.test_case_version_id}")
    
    # Set executed_at if not provided and status is not "Not Run"
    if not execution_in.executed_at and status.name != "Not Run":
        execution_in.executed_at = datetime.utcnow()
    
    execution = Execution(**execution_in.dict())
    db.add(execution)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise ValueError("Invalid foreign key reference")
        elif "unique constraint" in str(e).lower():
            raise ValueError("Duplicate execution for same run and test case version")
        else:
            raise ValueError(f"Database error: {e}")
    
    db.refresh(execution)
    return execution


def _resolve_test_case_versions(
    db: Session,
    test_suite_id: int,
    version_override: Optional[Dict[int, int]] = None
) -> List[Tuple[int, int]]:
    """
    Resolve test case versions for a test suite according to the resolution flow.
    
    Returns: List of tuples (test_case_id, test_case_version_id)
    """
    # Step 1: Identify the target test_suite
    test_suite = db.query(TestSuite).filter(TestSuite.id == test_suite_id).first()
    if not test_suite:
        raise ValueError(f"Test suite with ID {test_suite_id} does not exist")
    
    # Step 2: Fetch all test_cases assigned to the test_suite (via suitcase mapping)
    suitcases = db.query(Suitcase).filter(Suitcase.test_suite_id == test_suite_id).all()
    if not suitcases:
        raise ValueError(f"Test suite with ID {test_suite_id} has no test cases")
    
    resolved_versions = []
    
    for suitcase in suitcases:
        test_case_id = suitcase.test_case_id
        
        # Step 3: For each test_case, fetch related test_case_version rows
        test_case_versions = db.query(TestCaseVersion).filter(
            TestCaseVersion.test_case_id == test_case_id
        ).order_by(TestCaseVersion.id.desc()).all()
        
        if not test_case_versions:
            continue  # Skip test cases without versions
        
        # Step 4: Select exactly one test_case_version per test_case
        selected_version = None
        
        # Check for explicit override first
        if version_override and test_case_id in version_override:
            version_id = version_override[test_case_id]
            for version in test_case_versions:
                if version.id == version_id:
                    selected_version = version
                    break
        
        # Default: Choose test_case_version with the highest primary key
        if not selected_version:
            selected_version = test_case_versions[0]  # Already sorted by id.desc()
        
        resolved_versions.append((test_case_id, selected_version.id))
    
    return resolved_versions


def create_executions_for_test_suite(
    db: Session,
    run_id: int,
    test_suite_id: int,
    device_id: int,
    executed_by: int,
    version_override: Optional[Dict[int, int]] = None
) -> List[Execution]:
    """
    Create executions in bulk when test cases are assigned to a test suite.
    
    Follows the resolution flow:
    1. Identify test_suite
    2. Fetch test_cases via suitcase
    3. Resolve test_case_version for each test_case
    4. Create execution per resolved test_case_version
    """
    # Validate run exists
    run = db.query(Run).filter(Run.id == run_id).first()
    if not run:
        raise ValueError(f"Run with ID {run_id} does not exist")
    
    # Validate device exists
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise ValueError(f"Device with ID {device_id} does not exist")
    
    # Validate executor exists
    executor = db.query(Tester).filter(Tester.id == executed_by).first()
    if not executor:
        raise ValueError(f"Tester with ID {executed_by} does not exist")
    
    # Get "Not Run" status
    not_run_status = db.query(Status).filter(Status.name == "Not Run").first()
    if not not_run_status:
        raise ValueError("Status 'Not Run' not found")
    
    # Resolve test case versions
    resolved_versions = _resolve_test_case_versions(db, test_suite_id, version_override)
    
    executions = []
    execution_order = 1
    
    for test_case_id, test_case_version_id in resolved_versions:
        # Check if execution already exists
        existing = db.query(Execution).filter(
            and_(
                Execution.run_id == run_id,
                Execution.test_case_version_id == test_case_version_id
            )
        ).first()
        
        if existing:
            # Update execution order if needed
            if existing.execution_order != execution_order:
                existing.execution_order = execution_order
                executions.append(existing)
            execution_order += 1
            continue
        
        # Create new execution
        execution_data = ExecutionCreate(
            device_id=device_id,
            run_id=run_id,
            test_case_version_id=test_case_version_id,
            executed_by=executed_by,
            status_id=not_run_status.id,
            execution_order=execution_order,
            executed_at=None,
            actual_result=None,
            attachment_id=None
        )
        
        try:
            execution = create_execution(db, execution_data)
            executions.append(execution)
        except Exception as e:
            # Skip problematic executions but continue with others
            print(f"Failed to create execution for test case version {test_case_version_id}: {e}")
            continue
        
        execution_order += 1
    
    return executions


def update_execution(
    db: Session,
    execution_id: int,
    execution_in: ExecutionUpdate,
) -> Optional[Execution]:
    """Update an existing execution."""
    execution = get_execution_by_id(db, execution_id)
    if not execution:
        return None
    
    update_data = execution_in.dict(exclude_unset=True)
    
    # Restriction: test_case_version reference must not change after creation
    if "test_case_version_id" in update_data:
        if update_data["test_case_version_id"] != execution.test_case_version_id:
            raise ValueError("Cannot change test_case_version reference after creation")
    
    # Validate foreign keys if being updated
    if "device_id" in update_data:
        device = db.query(Device).filter(Device.id == update_data["device_id"]).first()
        if not device:
            raise ValueError(f"Device with ID {update_data['device_id']} does not exist")
    
    if "run_id" in update_data:
        run = db.query(Run).filter(Run.id == update_data["run_id"]).first()
        if not run:
            raise ValueError(f"Run with ID {update_data['run_id']} does not exist")
    
    if "executed_by" in update_data:
        tester = db.query(Tester).filter(Tester.id == update_data["executed_by"]).first()
        if not tester:
            raise ValueError(f"Tester with ID {update_data['executed_by']} does not exist")
    
    if "status_id" in update_data:
        status = db.query(Status).filter(Status.id == update_data["status_id"]).first()
        if not status:
            raise ValueError(f"Status with ID {update_data['status_id']} does not exist")
    
    if "attachment_id" in update_data and update_data["attachment_id"]:
        attachment = db.query(Attachment).filter(Attachment.id == update_data["attachment_id"]).first()
        if not attachment:
            raise ValueError(f"Attachment with ID {update_data['attachment_id']} does not exist")
    
    for field, value in update_data.items():
        setattr(execution, field, value)
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if "foreign key constraint" in str(e).lower():
            raise ValueError("Invalid foreign key reference")
        elif "unique constraint" in str(e).lower():
            raise ValueError("Duplicate execution for same run and test case version")
        else:
            raise ValueError(f"Database error: {e}")
    
    db.refresh(execution)
    return execution


def get_executions_by_run(db: Session, run_id: int) -> List[Execution]:
    """Get all executions for a specific run."""
    return db.query(Execution).filter(Execution.run_id == run_id).order_by(
        asc(Execution.execution_order),
        desc(Execution.executed_at)
    ).all()


def get_executions_by_device(db: Session, device_id: int) -> List[Execution]:
    """Get all executions on a specific device."""
    return db.query(Execution).filter(Execution.device_id == device_id).order_by(
        desc(Execution.executed_at)
    ).all()


def get_executions_by_tester(db: Session, tester_id: int) -> List[Execution]:
    """Get all executions performed by a specific tester."""
    return db.query(Execution).filter(Execution.executed_by == tester_id).order_by(
        desc(Execution.executed_at)
    ).all()


def get_executions_by_test_case(db: Session, test_case_id: int) -> List[Execution]:
    """Get all executions for a specific test case (across all versions)."""
    # Get all versions of the test case
    versions = db.query(TestCaseVersion.id).filter(
        TestCaseVersion.test_case_id == test_case_id
    ).subquery()
    
    return db.query(Execution).filter(
        Execution.test_case_version_id.in_(versions)
    ).order_by(desc(Execution.executed_at)).all()


def get_executions_by_test_suite(db: Session, test_suite_id: int) -> List[Execution]:
    """Get all executions for test cases in a specific test suite."""
    # Get test case IDs in the test suite
    test_case_ids = db.query(Suitcase.test_case_id).filter(
        Suitcase.test_suite_id == test_suite_id
    ).subquery()
    
    # Get versions of those test cases
    version_ids = db.query(TestCaseVersion.id).filter(
        TestCaseVersion.test_case_id.in_(test_case_ids)
    ).subquery()
    
    return db.query(Execution).filter(
        Execution.test_case_version_id.in_(version_ids)
    ).order_by(desc(Execution.executed_at)).all()


def get_execution_stats(db: Session, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get execution statistics."""
    query = db.query(
        Status.name,
        func.count(Execution.id).label('count')
    ).join(Status, Execution.status_id == Status.id)
    
    if filters:
        if filters.get("run_id"):
            query = query.filter(Execution.run_id == filters["run_id"])
        if filters.get("project_id"):
            query = query.join(Device).filter(Device.project_id == filters["project_id"])
        if filters.get("device_id"):
            query = query.filter(Execution.device_id == filters["device_id"])
        if filters.get("executed_by"):
            query = query.filter(Execution.executed_by == filters["executed_by"])
        if filters.get("executed_after"):
            query = query.filter(Execution.executed_at >= filters["executed_after"])
        if filters.get("executed_before"):
            query = query.filter(Execution.executed_at <= filters["executed_before"])
    
    results = query.group_by(Status.name).all()
    
    # Calculate totals
    total = sum(result.count for result in results)
    
    # Map results
    stats = {
        "total_executions": total,
        "passed_executions": 0,
        "failed_executions": 0,
        "in_progress_executions": 0,
        "blocked_executions": 0,
        "not_run_executions": 0,
        "completed_executions": 0,
        "by_status": {}
    }
    
    for result in results:
        stats["by_status"][result.name] = result.count
        
        if result.name == "Pass":
            stats["passed_executions"] = result.count
            stats["completed_executions"] += result.count
        elif result.name == "Fail":
            stats["failed_executions"] = result.count
            stats["completed_executions"] += result.count
        elif result.name == "Blocked":
            stats["blocked_executions"] = result.count
            stats["completed_executions"] += result.count
        elif result.name == "In Progress":
            stats["in_progress_executions"] = result.count
        elif result.name == "Not Run":
            stats["not_run_executions"] = result.count
        else:
            stats["completed_executions"] += result.count
    
    # Calculate average execution time for completed executions
    if filters and filters.get("run_id"):
        avg_time_query = db.query(
            func.avg(
                func.extract('epoch', Execution.executed_at) - 
                func.extract('epoch', Run.started_at)
            )
        ).join(Run, Execution.run_id == Run.id).filter(
            Execution.run_id == filters["run_id"],
            Execution.executed_at.isnot(None),
            Run.started_at.isnot(None)
        ).first()
        
        if avg_time_query and avg_time_query[0]:
            stats["average_execution_time_seconds"] = float(avg_time_query[0])
    
    return stats


def get_execution_with_relations(db: Session, execution_id: int) -> Optional[Dict[str, Any]]:
    """Get an execution with all related objects."""
    execution = db.query(Execution).filter(Execution.id == execution_id).first()
    if not execution:
        return None
    
    # Get all related data
    device = db.query(Device).filter(Device.id == execution.device_id).first()
    run = db.query(Run).filter(Run.id == execution.run_id).first()
    test_case_version = db.query(TestCaseVersion).filter(
        TestCaseVersion.id == execution.test_case_version_id
    ).first()
    executor = db.query(Tester).filter(Tester.id == execution.executed_by).first()
    status = db.query(Status).filter(Status.id == execution.status_id).first()
    attachment = db.query(Attachment).filter(Attachment.id == execution.attachment_id).first() if execution.attachment_id else None
    
    # Get test case for the version
    test_case = db.query(TestCase).filter(TestCase.id == test_case_version.test_case_id).first() if test_case_version else None
    
    return {
        "id": execution.id,
        "device_id": execution.device_id,
        "run_id": execution.run_id,
        "test_case_version_id": execution.test_case_version_id,
        "executed_by": execution.executed_by,
        "status_id": execution.status_id,
        "attachment_id": execution.attachment_id,
        "actual_result": execution.actual_result,
        "executed_at": execution.executed_at,
        "execution_order": execution.execution_order,
        "device": {
            "id": device.id,
            "name_external": device.name_external,
            "name_internal": device.name_internal,
            "project_id": device.project_id
        } if device else None,
        "run": {
            "id": run.id,
            "name": run.name,
            "project_id": run.project_id,
            "started_at": run.started_at,
            "done_at": run.done_at
        } if run else None,
        "test_case_version": {
            "id": test_case_version.id,
            "test_case_id": test_case_version.test_case_id,
            "version": test_case_version.version,
            "name": test_case_version.name,
            "description": test_case_version.description,
            "release_ready": test_case_version.release_ready
        } if test_case_version else None,
        "test_case": {
            "id": test_case.id,
            "scenario_id": test_case.scenario_id,
            "status_set_id": test_case.status_set_id
        } if test_case else None,
        "executor": {
            "id": executor.id,
            "email": executor.email,
            "first_name": executor.first_name,
            "last_name": executor.last_name
        } if executor else None,
        "status": {
            "id": status.id,
            "name": status.name,
            "description": status.description
        } if status else None,
        "attachment": {
            "id": attachment.id,
            "filename": attachment.filename,
            "relative_path": attachment.relative_path
        } if attachment else None
    }


def update_execution_status(
    db: Session,
    execution_id: int,
    status_id: int,
    actual_result: Optional[str] = None,
    attachment_id: Optional[int] = None
) -> Optional[Execution]:
    """Update an execution's status and related fields."""
    execution = get_execution_by_id(db, execution_id)
    if not execution:
        return None
    
    # Validate status
    status = db.query(Status).filter(Status.id == status_id).first()
    if not status:
        raise ValueError(f"Status with ID {status_id} does not exist")
    
    # Validate attachment if provided
    if attachment_id:
        attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
        if not attachment:
            raise ValueError(f"Attachment with ID {attachment_id} does not exist")

    # Update fields
    execution.status_id = status_id
    
    # Set executed_at if status is not "Not Run" and we're executing now
    if not execution.executed_at:
        execution.executed_at = datetime.utcnow()
    
    if actual_result is not None:
        execution.actual_result = actual_result
    
    if attachment_id is not None:
        execution.attachment_id = attachment_id
    
    db.commit()
    db.refresh(execution)
    return execution


def reassign_execution_device(
    db: Session,
    execution_id: int,
    new_device_id: int
) -> Optional[Execution]:
    """Reassign an execution to a different device."""
    execution = get_execution_by_id(db, execution_id)
    if not execution:
        return None
    
    # Validate new device
    new_device = db.query(Device).filter(Device.id == new_device_id).first()
    if not new_device:
        raise ValueError(f"Device with ID {new_device_id} does not exist")
    
    execution.device_id = new_device_id
    db.commit()
    db.refresh(execution)
    return execution


def reassign_execution_tester(
    db: Session,
    execution_id: int,
    new_tester_id: int
) -> Optional[Execution]:
    """Reassign an execution to a different tester."""
    execution = get_execution_by_id(db, execution_id)
    if not execution:
        return None
    
    # Validate new tester
    new_tester = db.query(Tester).filter(Tester.id == new_tester_id).first()
    if not new_tester:
        raise ValueError(f"Tester with ID {new_tester_id} does not exist")
    
    execution.executed_by = new_tester_id
    db.commit()
    db.refresh(execution)
    return execution