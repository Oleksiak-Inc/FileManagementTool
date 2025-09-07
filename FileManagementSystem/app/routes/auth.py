from flask import Blueprint, request
from db import db_connection
from app.services.auth_service import authenticate_user
from config import CONFIG

SQL_ADDRESS = CONFIG()["SQL_ADDRESS"]
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["POST"])
@db_connection(SQL_ADDRESS)
def login(conn):
    data = request.get_json()
    return authenticate_user(conn, data)
