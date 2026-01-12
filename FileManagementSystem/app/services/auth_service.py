from sql_loader import SQL_COMMANDS
from auth import authenticate

sql = SQL_COMMANDS()

def authenticate_user(cur, data):
    mail, password = data.get("email"), data.get("password")
    if not mail or not password:
        return {"status": "fail", "msg": "Email and password are required"}

    user = cur.execute(sql['get_private_user'], (mail,)).fetchone()
    if not user:
        return {"status": "fail", "msg": "User not found"}

    if authenticate(password=password, stored_hash_b64=user["password"]):
        return {
            "status": "success", 
            "user": dict(user),
            "msg": "Authentication successful"}
    return {"status": "fail", "msg": "Invalid credentials"}
