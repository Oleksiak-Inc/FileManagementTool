from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity,
    verify_jwt_in_request
)
from flask_smorest import Blueprint
from database.db_utils import db_route
from app.services.users_service import (
    get_all_users,
    get_user_by_mail,
    add_user,
    delete_user,
    is_bootstrap_allowed,
)
from app.schemas.user import (
    UserSchema,
    UserCreateSchema
)

users_bp = Blueprint(
    "users",
    "users",
    url_prefix="/users",
    description="User management"
)

@users_bp.route("/", methods=["GET"])
@users_bp.response(200, UserSchema(many=True))
@users_bp.doc(security=[{"bearerAuth": []}])
@jwt_required()
def list_users():
    return db_route(get_all_users)

@users_bp.route("/<string:mail>", methods=["GET"])
@users_bp.response(200, UserSchema(many=True))
@users_bp.doc(
    security=[{"bearerAuth": []}],
    parameters=[
        {
            "name": "mail",
            "in": "path",
            "required": True,
            "schema": {"type": "string"}
        }
    ]
)
@jwt_required()
def get_user(mail):
    return db_route(get_user_by_mail, mail)

@users_bp.route("/", methods=["POST"])
@users_bp.arguments(UserCreateSchema)
@users_bp.response(200, UserSchema)
@users_bp.doc(
    description="First user can be created without JWT (bootstrap). JWT required otherwise.")
def create_user(data):
    
    def handler(cur):
        if not is_bootstrap_allowed(cur):
            
            verify_jwt_in_request()

        return add_user(cur, data)

    return db_route(handler)

@users_bp.route("/<string:email>", methods=["DELETE"])
@users_bp.response(200, UserSchema)
@users_bp.doc(
    security=[{"bearerAuth": []}],
    parameters=[
        {
            "name": "email",
            "in": "path",
            "required": True,
            "schema": {"type": "string"}
        }
    ]
)
@jwt_required()
def remove_user(email):
    return db_route(delete_user, {"email": email})