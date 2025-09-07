from sql_loader import SQL_COMMANDS
from auth import hash_password

sql = SQL_COMMANDS()

def get_all_users(conn):
    users = conn.execute(sql['get_public_users']).fetchall()
    return {"status": "success", "message": [dict(row) for row in users]}

def get_user_by_mail(conn, mail):
    user = conn.execute(sql['get_public_user'], (mail,)).fetchone()
    if user:
        return {"status": "success", "message": [dict(user)]}
    return {"status": "fail", "message": "User not found"}

def add_user(conn, data):
    name, email, password = data.get("name"), data.get("email"), data.get("password")
    hashed_password = hash_password(password)
    conn.execute(sql['add_user'], (name, email, hashed_password))
    conn.commit()
    return {"status": "success", "message": f"User {name} added"}

def delete_user(conn, data):
    email = data.get("email")
    conn.execute(sql['delete_user'], (email,))
    conn.commit()
    return {"status": "success", "message": f"Deleted {email}"}
