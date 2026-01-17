from flask import Blueprint, request
from ..services.auth_service import AuthService

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post("/login")
def login():
    data = request.json
    token = AuthService.login(data["email"], data["password"])
    return {"access_token": token}
