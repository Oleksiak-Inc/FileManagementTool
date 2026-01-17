from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.test_case_service import TestCaseService
from ..schemas.test_case import TestCaseVersionSchema
from ..utils.permissions import require_user_type

bp = Blueprint("test_cases", __name__, url_prefix="/test-cases")

@bp.post("/<int:test_case_id>/versions")
@jwt_required()
@require_user_type("admin", "super")
def create_version(test_case_id):
    user_id = get_jwt_identity()
    version = TestCaseService.create_version(test_case_id, user_id, request.json)
    return TestCaseVersionSchema().dump(version), 201
