import bcrypt, base64

import db
from main import SQL_ADDRES
from sql_loader import SQL_COMMANDS

sql_commands = SQL_COMMANDS().SQL_DICT

def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_b64 = base64.b64encode(hashed).decode('utf-8')
    return hashed_b64

@db.db_connection(SQL_ADDRES)
def auth_user(conn, request, sql, params):
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
    
        if not email or not password:
            return {"status": "fail", "message": "Email and password are required"}

        user = conn.execute(sql, params)

        if user is None:
            return {"status": "fail", "message": "User not found"}

        stored_hash = user["password"]  # this is a string from DB
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return {"status": "success", "message": "Authentication successful"}
        else:
            return {"status": "fail", "message": "Invalid credentials"}


    except Exception as e:
        return {"status": "fail", "message": f"Error: {e}"}