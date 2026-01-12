from sql_loader import SQL_COMMANDS
from auth import hash_password

sql = SQL_COMMANDS()

# ------------------------
# READ
# ------------------------
def get_all_users(cur):
    users = cur.execute(sql["get_public_users"]).fetchall()
    return [dict(row) for row in users]


def get_user_by_mail(cur, mail):
    user = cur.execute(sql["get_public_user"], (mail,)).fetchone()
    return dict(user) if user else None

# ------------------------
# CREATE
# ------------------------
def add_user(cur, data):
    hashed_password = hash_password(data["password"])

    cur.execute(
        sql["add_user"],
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
        sql["get_public_user"],
        (data["email"],),
    ).fetchone()

    return dict(user)


# ------------------------
# DELETE
# ------------------------
def delete_user(cur, email):
    res = cur.execute("DELETE FROM \"user\" WHERE email=%s RETURNING id", (email,))
    row = res.fetchone()
    if not row:
        return None  # triggers 404 in route
    return True
