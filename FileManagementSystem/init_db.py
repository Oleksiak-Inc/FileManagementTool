# --- /home/oleksiak/FileManagementTool/FileManagementSystem/init_db.py ---
import os
from pathlib import Path
import time
from functools import wraps
from sqlalchemy.exc import OperationalError
from app.database.session import engine, SessionLocal
from app.database.base import Base
from app.database.models import (
    TesterType, Status, StatusSet, TestCase, Scenario,
    Tester, TestCaseVersion, TesterGroup, Client, Project,
    Device, Resolution, TestSuite
)
from app.utils.auth import hash_password
from app.config import settings

def retry_on_operational_error(max_retries=30, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except OperationalError as e:
                    if attempt < max_retries:
                        print(f"[INIT] Attempt {attempt}/{max_retries} failed: {e}")
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

@retry_on_operational_error()
def create_tables_and_data():
    print(f"[INIT] Using DB at: {settings.DATABASE_URL}")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:

        uploads_dir = Path(__file__).parent / "uploads"
        uploads_dir.mkdir(exist_ok=True)
    
        print(f"[INIT] Created uploads directory at: {uploads_dir}")

        # Create tester types
        tester_types = [
            {"name": "super", "description": "SuperTester"},
            {"name": "admin", "description": "Administrator"},
            {"name": "regular", "description": "Default regular tester"},
        ]

        for data in tester_types:
            if not db.query(TesterType).filter_by(name=data["name"]).first():
                db.add(TesterType(**data))

        db.flush()

        # Create default status sets with statuses
        default_status_sets = [
            {
                "name": "Test Execution",
                "statuses": [
                    {"name": "Pass", "description": "Test passed successfully"},
                    {"name": "Fail", "description": "Test failed"},
                    {"name": "Blocked", "description": "Test blocked by issue"},
                    {"name": "Not Run", "description": "Test not executed"},
                    {"name": "Not Implemented", "description": "Feature not implemented"},
                    {"name": "In Progress", "description": "Test currently running"},
                ]
            },
        ]

        for set_data in default_status_sets:
            status_set = db.query(StatusSet).filter_by(name=set_data["name"]).first()
            if not status_set:
                status_set = StatusSet(name=set_data["name"])
                db.add(status_set)
                db.flush()  # Get the ID
                
                # Add statuses for this set
                for status_data in set_data["statuses"]:
                    status = Status(
                        name=status_data["name"],
                        description=status_data["description"],
                        status_set_id=status_set.id
                    )
                    db.add(status)

        # Create default scenarios
        default_scenarios = [
            {"name": "Login Test"},
            {"name": "Performance Test"},
            {"name": "Security Test"},
            {"name": "UI Test"},
        ]

        for scenario_data in default_scenarios:
            if not db.query(Scenario).filter_by(name=scenario_data["name"]).first():
                db.add(Scenario(**scenario_data))

        # Create default test suites
        default_test_suites = [
            {"name": "Smoke Test Suite"},
            {"name": "Regression Test Suite"},
            {"name": "Integration Test Suite"},
        ]

        for suite_data in default_test_suites:
            if not db.query(TestSuite).filter_by(name=suite_data["name"]).first():
                db.add(TestSuite(**suite_data))

        # Create default resolutions
        default_resolutions = [
            {"w": 1920, "h": 1080},
            {"w": 2560, "h": 1440},
            {"w": 3840, "h": 2160},
            {"w": 1280, "h": 720},
        ]

        for res_data in default_resolutions:
            if not db.query(Resolution).filter_by(w=res_data["w"], h=res_data["h"]).first():
                db.add(Resolution(**res_data))

        # Create default clients
        default_clients = [
            {"name": "Default Client"},
            {"name": "Internal Testing"},
        ]

        for client_data in default_clients:
            if not db.query(Client).filter_by(name=client_data["name"]).first():
                db.add(Client(**client_data))

        db.flush()

        # Create default projects (requires clients)
        default_projects = [
            {"name": "Main Project", "client_id": 1},
            {"name": "Internal Project", "client_id": 2},
        ]

        for project_data in default_projects:
            if not db.query(Project).filter_by(name=project_data["name"]).first():
                # Verify client exists
                client = db.query(Client).filter_by(id=project_data["client_id"]).first()
                if client:
                    db.add(Project(**project_data))

        db.flush()

        # Create default devices (requires projects)
        default_devices = [
            {
                "name_external": "Test Device 1",
                "name_internal": "DEV-001",
                "cpu": "Intel Core i7",
                "gpu": "NVIDIA RTX 3080",
                "ram": "32GB",
                "project_id": 1
            },
            {
                "name_external": "Test Device 2",
                "name_internal": "DEV-002",
                "cpu": "AMD Ryzen 9",
                "gpu": "AMD Radeon RX 6800",
                "ram": "64GB",
                "project_id": 1
            },
        ]

        for device_data in default_devices:
            if not db.query(Device).filter_by(name_internal=device_data["name_internal"]).first():
                # Verify project exists
                project = db.query(Project).filter_by(id=device_data["project_id"]).first()
                if project:
                    db.add(Device(**device_data))

        # Create default tester groups
        default_tester_groups = [
            {"name": "QA Team", "created_by_id": None, "owner_id": None},
            {"name": "Development Team", "created_by_id": None, "owner_id": None},
        ]

        # Create default admin tester if none exists
        default_tester = db.query(Tester).filter_by(email="admin@example.com").first()
        if not default_tester:
            # Get super tester type
            super_type = db.query(TesterType).filter_by(name="super").first()
            
            default_tester = Tester(
                email="admin@example.com",
                first_name="Admin",
                last_name="User",
                password=hash_password("admin123"),
                tester_type_id=super_type.id if super_type else 1,
                active=True
            )
            db.add(default_tester)
            db.flush()

        # Update tester groups with the created_by and owner IDs
        for group_data in default_tester_groups:
            if not db.query(TesterGroup).filter_by(name=group_data["name"]).first():
                group_data["created_by_id"] = default_tester.id
                group_data["owner_id"] = default_tester.id
                db.add(TesterGroup(**group_data))

        # Create additional regular testers
        regular_testers = [
            {
                "email": "tester1@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "password123",
                "tester_type_id": 3  # regular
            },
            {
                "email": "tester2@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "password": "password123",
                "tester_type_id": 3  # regular
            },
        ]

        for tester_data in regular_testers:
            if not db.query(Tester).filter_by(email=tester_data["email"]).first():
                # Get regular tester type
                regular_type = db.query(TesterType).filter_by(name="regular").first()
                
                tester = Tester(
                    email=tester_data["email"],
                    first_name=tester_data["first_name"],
                    last_name=tester_data["last_name"],
                    password=hash_password(tester_data["password"]),
                    tester_type_id=regular_type.id if regular_type else 3,
                    active=True
                )
                db.add(tester)

        db.flush()

        # Create sample test cases if none exist
        if db.query(TestCase).count() == 0:
            # Get first scenario and status set
            first_scenario = db.query(Scenario).first()
            first_status_set = db.query(StatusSet).first()
            
            if first_scenario and first_status_set:
                test_cases_data = [
                    {"scenario_id": first_scenario.id, "status_set_id": first_status_set.id},
                    {"scenario_id": first_scenario.id, "status_set_id": first_status_set.id},
                ]
                
                for tc_data in test_cases_data:
                    test_case = TestCase(**tc_data)
                    db.add(test_case)
        
        db.flush()

        # Create sample test case versions if none exist
        if db.query(TestCaseVersion).count() == 0:
            # Get test cases
            test_cases = db.query(TestCase).all()
            
            for i, test_case in enumerate(test_cases):
                version_data = {
                    "test_case_id": test_case.id,
                    "created_by": default_tester.id,
                    "version": 1,
                    "name": f"Initial Version - Test Case {test_case.id}",
                    "description": f"This is the initial version of test case {test_case.id}",
                    "steps": f"1. Step one for test case {test_case.id}\n2. Step two\n3. Step three",
                    "expected_result": f"Test case {test_case.id} passes when all steps are completed successfully",
                    "release_ready": True if i % 2 == 0 else False  # Alternate release readiness
                }
                
                version = TestCaseVersion(**version_data)
                db.add(version)

        db.commit()
        print("[INIT] Database initialized successfully with default data")
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        print(f"[INIT] Error initializing database: {e}")
        raise
    finally:
        db.close()

def init_db():
    return create_tables_and_data()

if __name__ == "__main__":
    init_db()