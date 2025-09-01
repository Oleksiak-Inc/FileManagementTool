from flask import Flask, jsonify, request
import sqlite3 as sql
import bcrypt, base64

import sql_loader

app = Flask(__name__)
sql_commands = sql_loader.SQL_COMMANDS().SQL_DICT

def get_db_connection():
    conn = sql.connect('example.db')
    conn.execute(sql_commands['create_table_users'])
    conn.row_factory = sql.Row  # makes rows dict-like
    return conn

def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    hashed_b64 = base64.b64encode(hashed).decode('utf-8')
    return hashed_b64

@app.route('/users', methods=['GET'])
def get_users():
    try:
        with get_db_connection() as conn:
            users = conn.execute(sql_commands['get_users']).fetchall()
        return jsonify({"status": "success", "message": [dict(row) for row in users]})
    except Exception as e:
        return jsonify({"status": "fail", "message": f"Cannot fetch data. Error: {e}"})

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        with get_db_connection() as conn:
            users = conn.execute(sql_commands['get_user'], (id, )).fetchall()
        return jsonify({"status": "success", "message": [dict(row) for row in users]})
    except Exception as e:
        return jsonify({"status": "fail", "message": f"Cannot fetch data. Error: {e}"})

@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('pass')
        hashed_password = encrypt_password(password)
        with get_db_connection() as conn:
            conn.execute(sql_commands['add_user'], (name, email, hashed_password))
            conn.commit()
        return jsonify({"status": "success", "message": f"User {name} added"})
    except Exception as e:
        return jsonify({"status": "fail", "message":f"Cannot add an user. Error: {e}"})

@app.route('/users', methods=['DELETE'])
def del_user():
    try:
        data = request.get_json()
        email = data.get('email')
        with get_db_connection() as conn:
            conn.execute(sql_commands['delete_user'], (email,))
            conn.commit()
        return jsonify({"status": "success", "message":f"Deleted {email}"})
    except Exception as e:
        return jsonify({"status": "fail", "message": f"Cannot delete {email}. Error: {e}"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)