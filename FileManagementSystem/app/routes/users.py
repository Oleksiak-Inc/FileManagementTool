from flask import Blueprint, request
from db import db_connection
from app.services.users_service import get_all_users, get_user_by_mail, add_user, delete_user
from config import CONFIG

SQL_ADDRESS = CONFIG()["SQL_ADDRESS"]
users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
@db_connection(SQL_ADDRESS)
def list_users(conn):
    return get_all_users(conn)

@users_bp.route("/<string:mail>", methods=["GET"])
@db_connection(SQL_ADDRESS)
def get_user(conn, mail):
    return get_user_by_mail(conn, mail)

@users_bp.route("/", methods=["POST"])
@db_connection(SQL_ADDRESS)
def create_user(conn):
    data = request.get_json()
    return add_user(conn, data)

@users_bp.route("/", methods=["DELETE"])
@db_connection(SQL_ADDRESS)
def remove_user(conn):
    data = request.get_json()
    return delete_user(conn, data)
