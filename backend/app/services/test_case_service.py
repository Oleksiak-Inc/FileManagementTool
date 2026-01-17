from ..models import TestCase, TestCaseVersion
from ..extensions import db

class TestCaseService:

    @staticmethod
    def create_version(test_case_id, user_id, data):
        latest = (
            TestCaseVersion.query
            .filter_by(test_case_id=test_case_id)
            .order_by(TestCaseVersion.version.desc())
            .first()
        )
        next_version = 1 if not latest else latest.version + 1

        version = TestCaseVersion(
            test_case_id=test_case_id,
            created_by=user_id,
            version=next_version,
            **data
        )
        db.session.add(version)
        db.session.commit()
        return version
