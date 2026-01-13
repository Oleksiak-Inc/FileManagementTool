from sql_loader import SQL_COMMANDS
from auth import authenticate

sql = SQL_COMMANDS()

def authenticate_user(cur, data):
    user = cur.execute(sql["user"]["get_private_user"], (data["email"],)).fetchone()
    if not user:
        return None

    if authenticate(password=data["password"], stored_hash_b64=user["password"]):
        return dict(user)

    return None
