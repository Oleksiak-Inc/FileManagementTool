from sql_loader import SQL_COMMANDS
from auth import hash_password

sql = SQL_COMMANDS()

# ------------------------
# READ
# ------------------------
def get_all_users(cur):
    users = cur.execute(sql["user"]["get_public_users"]).fetchall()
    return [dict(row) for row in users]


def get_user_by_mail(cur, mail):
    user = cur.execute(sql["user"]["get_public_user"], (mail,)).fetchone()
    return dict(user) if user else None

# ------------------------
# CREATE
# ------------------------
def add_user(cur, data):
    hashed_password = hash_password(data["password"])

    cur.execute(
        sql["user"]["add_user"],
        (
            data["first_name"],
            data["last_name"],
            data["email"],
            hashed_password,
            data.get("user_type_id"),
        ),
    )

    # Fetch created user (important for Swagger)
    user = cur.execute(
        sql["user"]["get_public_user"],
        (data["email"],),
    ).fetchone()

    return dict(user)
