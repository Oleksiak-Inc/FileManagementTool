from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_smorest import Blueprint
from app.services.auth_service import authenticate_user
from database.db_utils import db_route
from app.schemas.auth import LoginSchema, TokenSchema

auth_bp = Blueprint(
    "auth",
    "auth",
    url_prefix="/auth",
    description="Authentication"
)

@auth_bp.route("/", methods=["POST"])
@auth_bp.arguments(LoginSchema)
@auth_bp.response(200, TokenSchema)
def login(data):
    result = db_route(authenticate_user, data)
    if result["status"] != "success":
        return jsonify(result), 401

    token = create_access_token(
        identity=str(result["user"]["id"]),
        additional_claims={
            "email": result["user"]["email"],
            "user_type_id": result["user"]["user_type_id"]
        }
    )

    return {
        "status": "success",
        "access_token": token
    }

