from sql_loader import SQL_COMMANDS
from auth import authenticate

sql = SQL_COMMANDS()

def authenticate_user(conn, data):
    mail, password = data.get("email"), data.get("password")
    if not mail or not password:
        return {"status": "fail", "message": "Email and password are required"}

    user = conn.execute(sql['get_private_user'], (mail,)).fetchone()
    if not user:
        return {"status": "fail", "message": "User not found"}

    stored_hash_b64 = user["password"]
    if authenticate(password=password, stored_hash_b64=stored_hash_b64):
        return {"status": "success", "message": "Authentication successful"}
    return {"status": "fail", "message": "Invalid credentials"}
