from psycopg import Cursor, connect
from psycopg.rows import dict_row

from config import CONFIG

SQL_ADDRESS = CONFIG()["SQL_ADDRESS"]

class DBCursor:
    def __init__(self):
        self.conn = None
        self.cur = None

    def __enter__(self) -> Cursor:
        self.conn = connect(SQL_ADDRESS)
        self.cur = self.conn.cursor(row_factory=dict_row)
        self.cur.execute("SET search_path TO public")
        return self.cur

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        self.cur.close()
        self.conn.close()

        # False = re-raise exception (important!)
        return False