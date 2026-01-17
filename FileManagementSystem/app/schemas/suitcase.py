# --- /home/oleksiak/FileManagementTool/FileManagementSystem/app/schemas/suitcase.py ---
from typing import Optional, List
from pydantic import BaseModel


class SuitcaseBase(BaseModel):
    test_case_id: int
    test_suite_id: int


class SuitcaseCreate(SuitcaseBase):
    pass


class SuitcaseResponse(SuitcaseBase):
    id: int
    
    class Config:
        from_attributes = True


class TestSuiteWithTestCasesResponse(BaseModel):
    test_suite_id: int
    test_suite_name: str
    test_cases: List[dict]  # List of test cases with their details
    
    class Config:
        from_attributes = True


class TestCaseWithTestSuitesResponse(BaseModel):
    test_case_id: int
    test_suites: List[dict]  # List of test suites with their details
    
    class Config:
        from_attributes = True


class AddTestCaseToSuiteRequest(BaseModel):
    test_case_id: int


class AddTestSuiteToCaseRequest(BaseModel):
    test_suite_id: int


class BulkAddTestCasesRequest(BaseModel):
    test_case_ids: List[int]


class BulkAddTestSuitesRequest(BaseModel):
    test_suite_ids: List[int]