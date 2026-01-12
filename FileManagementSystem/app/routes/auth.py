from flask_jwt_extended import create_access_token
from flask_smorest import Blueprint, abort
from app.schemas.auth import LoginSchema, TokenSchema
from app.schemas.error import ErrorSchema  # ADD THIS IMPORT
from app.services.auth_service import authenticate_user
from database.db_utils import db_route

auth_bp = Blueprint(
    "auth",
    "auth",
    url_prefix="/auth",
    description="Authentication",
)

@auth_bp.route("/", methods=["POST"])
@auth_bp.arguments(LoginSchema)
@auth_bp.response(200, TokenSchema)
@auth_bp.alt_response(401, schema=ErrorSchema)  # ADD THIS LINE
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