from flask_jwt_extended import create_access_token
from flask_smorest import Blueprint, abort
from app.schemas.auth import LoginSchema, TokenSchema
from app.schemas.error import ErrorSchema
from app.services.auth_service import authenticate_user
from app.routes.db import db_route

auth_bp = Blueprint(
    "auth",
    "auth",
    url_prefix="/auth",
    description="Authentication",
)

# Create method-specific decorators for auth
def auth_post(response_schema, arguments_schema=None, alt_response=None):
    """Decorator for auth POST endpoints"""
    def decorator(f):
        if arguments_schema:
            f = auth_bp.arguments(arguments_schema)(f)
        f = auth_bp.response(200, response_schema)(f)
        if alt_response:
            f = auth_bp.alt_response(alt_response[0], schema=alt_response[1])(f)
        return f
    return decorator

# No auth_get needed for now, but you can add it if you have GET endpoints later
def auth_get(response_schema, alt_response=None):
    """Decorator for auth GET endpoints"""
    def decorator(f):
        f = auth_bp.response(200, response_schema)(f)
        if alt_response:
            f = auth_bp.alt_response(alt_response[0], schema=alt_response[1])(f)
        return f
    return decorator

# Now the login endpoint becomes much cleaner
@auth_bp.route("/", methods=["POST"])
@auth_post(TokenSchema, arguments_schema=LoginSchema, alt_response=(401, ErrorSchema))
def login(data):
    user = db_route(authenticate_user, data)
    if not user:
        abort(401, message="Invalid credentials")

    token = create_access_token(
        identity=str(user["id"]),
        additional_claims={
            "email": user["email"],
            "user_type_id": user["user_type_id"],
        },
    )

    return {"access_token": token}