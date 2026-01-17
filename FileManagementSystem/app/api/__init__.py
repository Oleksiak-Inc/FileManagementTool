from fastapi import APIRouter
from .v1 import (
    auth,
    tester,
    device,
    resolution,
    client,
    scenario,
    status_set,
    test_suite,
    tester_type,
    project,
    status,
    test_case,
    test_case_version,
    attachment,
    run,
    suitcase,
    tester_group,
    execution
)

from .v1.admin import (
    tester as tester_admin, 
    tester_groups as tester_groups_admin, 
    tester_type as tester_type_admin
)

api_router = APIRouter()

api_router.include_router(tester_admin.router)
api_router.include_router(tester_groups_admin.router)
api_router.include_router(tester_type_admin.router)

api_router.include_router(auth.router)
api_router.include_router(tester.router)
api_router.include_router(device.router)
api_router.include_router(resolution.router)
api_router.include_router(client.router)
api_router.include_router(scenario.router)
api_router.include_router(status_set.router)
api_router.include_router(test_suite.router)
api_router.include_router(tester_type.router)
api_router.include_router(project.router)
api_router.include_router(status.router)
api_router.include_router(test_case.router)
api_router.include_router(test_case_version.router)
api_router.include_router(attachment.router)
api_router.include_router(run.router)
api_router.include_router(suitcase.router)
api_router.include_router(tester_group.router)
api_router.include_router(execution.router)