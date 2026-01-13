from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from app.routes.db import db_route
from app.services.users_service import (
    get_all_users,
    get_user_by_mail,
    add_user
)
from app.schemas.user import (
    UserSchema, 
    UserCreateSchema)
from app.schemas.error import ErrorSchema

users_bp = Blueprint(
    "users",
    "users",
    url_prefix="/users",
    description="User management"
)

# Custom decorators for specific HTTP methods
def get_response(response_schema=None, alt_response=None):
    def decorator(f):
        if response_schema:
            f = users_bp.response(200, response_schema)(f)
        if alt_response:
            f = users_bp.alt_response(alt_response[0], schema=alt_response[1])(f)
        f = users_bp.doc(security=[{"bearerAuth": []}])(f)
        f = jwt_required()(f)
        return f
    return decorator

def post_response(response_schema, alt_response=None, arguments_schema=None):
    def decorator(f):
        if arguments_schema:
            f = users_bp.arguments(arguments_schema)(f)
        f = users_bp.response(201, response_schema)(f)
        if alt_response:
            f = users_bp.alt_response(alt_response[0], schema=alt_response[1])(f)
        f = users_bp.doc(security=[{"bearerAuth": []}])(f)
        f = jwt_required()(f)
        return f
    return decorator

def delete_response(response_schema, alt_response=None):
    def decorator(f):
        if response_schema:
            f = users_bp.response(200, response_schema)(f)
        if alt_response:
            f = users_bp.alt_response(alt_response[0], schema=alt_response[1])(f)
        f = users_bp.doc(security=[{"bearerAuth": []}])(f)
        f = jwt_required()(f)
        return f
    return decorator

# READ
@users_bp.route("/", methods=["GET"])
@get_response(UserSchema(many=True))
def list_users():
    return db_route(get_all_users)

@users_bp.route("/<string:mail>", methods=["GET"])
@get_response(UserSchema, alt_response=(404, ErrorSchema))
def get_user(mail):
    user = db_route(get_user_by_mail, mail)
    if not user:
        abort(404, message="User not found")
    return user

# CREATE
@users_bp.route("/", methods=["POST"])
@post_response(UserSchema, alt_response=(409, ErrorSchema), 
               arguments_schema=UserCreateSchema)
def create_user(data):
    return db_route(add_user, data)