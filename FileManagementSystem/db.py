import functools
import sqlite3 as sql
from flask import jsonify

def db_connection(addr, return_json: bool=True):
    def connect(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with sql.connect(addr) as conn:
                conn.row_factory = sql.Row
                if return_json:
                    return jsonify(func(*args, conn=conn, **kwargs))
                else:
                    return func(*args, conn=conn, **kwargs)
        return wrapper
    return connect

def create_table():
    return 0
