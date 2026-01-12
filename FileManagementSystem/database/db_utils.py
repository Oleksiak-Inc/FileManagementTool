from database.db import DBCursor

def db_route(service_func, *args, **kwargs):
    with DBCursor() as cur:
        result = service_func(cur, *args, **kwargs)
    return result
