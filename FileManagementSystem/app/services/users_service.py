from sql_loader import SQL_COMMANDS
from app.services.query_builder import build_where_clause
from sql.user.filter_user import USER_FILTERS
from auth import hash_password

sql = SQL_COMMANDS()
# ------------------------
# READ
# ------------------------
def get_users_service(cur, filters=None):
    
    base_query = sql["user"]["get_public_user"]

    if filters:
        where_clause, values = build_where_clause(USER_FILTERS, filters)
        #print(where_clause)
        full_query = f"{base_query} {where_clause}"
        users = cur.execute(full_query, values).fetchall()
    else:
        users = cur.execute(base_query).fetchall()
    return [dict(row) for row in users]


def get_user_by_mail(cur, mail):
    '''user = cur.execute(sql["user"]["get_public_user"], (mail,)).fetchone()
    return dict(user) if user else None'''

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
