from sql_loader import SQL_COMMANDS
from auth import hash_password

sql = SQL_COMMANDS()

# ------------------------
# BOOTSTRAP CHECK
# ------------------------
def is_bootstrap_allowed(cur):
    return cur.execute(sql["user_count"]).fetchone()[0] == 0


# ------------------------
# READ
# ------------------------
def get_all_users(cur):
    users = cur.execute(sql["get_public_users"]).fetchall()
    return {
        "status": "success",
        "msg": [dict(row) for row in users]
    }


def get_user_by_mail(cur, mail):
    user = cur.execute(sql["get_public_user"], (mail,)).fetchone()
    if user:
        return {
            "status": "success",
            "msg": [dict(user)]
        }
    return {
        "status": "fail",
        "msg": "User not found"
    }


# ------------------------
# CREATE
# ------------------------
def add_user(cur, data):
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    password = data["password"]

    hashed_password = hash_password(password)

    # Bootstrap user becomes admin
    if is_bootstrap_allowed(cur):
        user_type_id = 2  # <-- admin role ID (adjust if needed)
    else:
        user_type_id = data.get("user_type_id")

    cur.execute(
        sql["add_user"],
        (first_name, last_name, email, hashed_password, user_type_id)
    )

    return {
        "status": "success",
        "msg": f"User {first_name} {last_name} added"
    }


# ------------------------
# DELETE
# ------------------------
def delete_user(cur, data):
    email = data["email"]

    cur.execute(sql["delete_user"], (email,))
    return {
        "status": "success",
        "msg": f"Deleted {email}"
    }
