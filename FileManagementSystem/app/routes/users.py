from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask import request

from app.routes.db import db_route
from app.services.users_service import get_users_service
from app.schemas.user_schema import UserSchema
from app.schemas.error_schema import ErrorSchema
from app.schemas.query_builder_schema import build_query_schema
from sql.user.filter_user import USER_FILTERS

users_bp = Blueprint(
    "users",
    "users",
    url_prefix="/users",
    description="User management"
)

# Build query schema ONCE for Swagger + validation
UserFilterSchema = build_query_schema("UserFilter", USER_FILTERS)

@users_bp.route("", methods=["GET"])
@users_bp.arguments(UserFilterSchema, location="query")
@users_bp.response(200, UserSchema(many=True))
@users_bp.alt_response(400, schema=ErrorSchema)
@users_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_users(filters):
    """
    Get users with optional query filters
    """
    return db_route(get_users_service, filters=filters)
