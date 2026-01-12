from database.db import DBCursor
from psycopg import errors
from flask_smorest import abort

def db_route(service_func, *args, **kwargs):
    with DBCursor() as cur:
        try:
            return service_func(cur, *args, **kwargs)

        except errors.UniqueViolation:
            cur.connection.rollback()
            abort(409, message="Resource already exists")

        except errors.ForeignKeyViolation:
            cur.connection.rollback()
            abort(409, message="Foreign key constraint violated")

        except Exception as e:
            cur.connection.rollback()
            abort(500, message=str(e))