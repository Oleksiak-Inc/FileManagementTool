from flask import Flask, jsonify, request

import db
from main import SQL_ADDRES
from sql_loader import SQL_COMMANDS
from auth import encrypt_password, authenticate

app = Flask(__name__)
sql_commands = SQL_COMMANDS().SQL_DICT

def run(debug: bool, host: str, port: int):
    app.run(debug=debug, host=host, port=port)

@app.route('/users', methods=['GET'], strict_slashes=False)
@db.db_connection(SQL_ADDRES)
def get_users(conn):
    try:
        users = conn.execute(sql_commands['get_users']).fetchall()
        return {"status": "success", "message": [dict(row) for row in users]}
    except Exception as e:
        return {"status": "fail", "message": f"Cannot fetch data. Error: {e}"}

@app.route('/users/<mail>', methods=['GET'], strict_slashes=False)
@db.db_connection(SQL_ADDRES)
def get_user(conn, mail):
    try:
        user = conn.execute(sql_commands['get_user'], (mail, )).fetchone()
        if user:
            return {"status": "success", "message": [user]}
        else:
            return {"status": "fail", "message": "User does not exist"}
    except Exception as e:
        return {"status": "fail", "message": f"Cannot fetch data. Error: {e}"}

@app.route('/auth', methods=['POST'], strict_slashes=False)
@db.db_connection(SQL_ADDRES)
def auth_user(conn, mail):
    try:
        user = conn.execute(sql_commands['get_user'], (mail, )).fetchone()
        if not user:
            return {"status": "fail", "message": "User not found"}
        
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return {"status": "fail", "message": "Email and password are required"}
        
        stored_hash_b64 = user["password"]
        auth_result = authenticate(password=password,stored_hash_b64=stored_hash_b64)
        if auth_result:
            return {"status": "success", "message": "Authentication successful"}
        else:
            return {"status": "fail", "message": f"Cannot authenticate. Error: Invalid credentials"}
            
    except Exception as e:
        return {"status": "fail", "message": f"Cannot authenticate. Error: {e}"}

@app.route('/users', methods=['POST'], strict_slashes=False)
@db.db_connection(SQL_ADDRES)
def add_user(conn):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        hashed_password = encrypt_password(password)
        conn.execute(sql_commands['add_user'], (name, email, hashed_password))
        conn.commit()
        return {"status": "success", "message": f"User {name} added"}
    except Exception as e:
        return {"status": "fail", "message":f"Cannot add an user. Error: {e}"}

@app.route('/users', methods=['DELETE'], strict_slashes=False)
@db.db_connection(SQL_ADDRES)
def del_user(conn):
    try:
        data = request.get_json()
        email = data.get('email')
        conn.execute(sql_commands['delete_user'], (email,))
        conn.commit()
        return {"status": "success", "message":f"Deleted {email}"}
    except Exception as e:
        return {"status": "fail", "message": f"Cannot delete {email}. Error: {e}"}

if __name__ == '__main__':
    run(debug=True, host='0.0.0.0', port=5000)