from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from database.db_utils import db_route
from app.services.users_service import (
    get_all_users,
    get_user_by_mail,
    add_user,
    delete_user
)
from app.schemas.user import UserSchema, UserCreateSchema
from app.schemas.error import ErrorSchema

users_bp = Blueprint(
    "users",
    "users",
    url_prefix="/users",
    description="User management"
)

# READ
@users_bp.route("/", methods=["GET"])
@users_bp.response(200, UserSchema(many=True))
@users_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def list_users():
    return db_route(get_all_users)

@users_bp.route("/<string:mail>", methods=["GET"])
@users_bp.response(200, UserSchema)
@users_bp.alt_response(404, schema=ErrorSchema)  # FIXED: Use schema= parameter
@users_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def get_user(mail):
    user = db_route(get_user_by_mail, mail)
    if not user:
        abort(404, message="User not found")
    return user

# CREATE
@users_bp.route("/", methods=["POST"])
@users_bp.arguments(UserCreateSchema)
@users_bp.response(201, UserSchema)
@users_bp.alt_response(409, schema=ErrorSchema)  # FIXED: Use schema= parameter
@users_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def create_user(data):
    return db_route(add_user, data)

# DELETE
@users_bp.route("/<string:email>", methods=["DELETE"])
@users_bp.response(204)
@users_bp.alt_response(404, schema=ErrorSchema)  # FIXED: Use schema= parameter
@users_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def remove_user(email):
    db_route(delete_user, email)