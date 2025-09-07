import functools
import sqlite3 as sql
from flask import jsonify

def db_connection(addr: str, return_json: bool=True):
    def connect(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with sql.connect(addr) as conn:
                conn.row_factory = sql.Row
                if return_json:
                    return jsonify(func(*args, conn=conn, **kwargs))
                else:
                    return func(conn=conn)
        return wrapper
    return connect
