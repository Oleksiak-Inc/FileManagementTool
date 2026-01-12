from app.services.db_init_service import initialize_database
from database.db import DBCursor
from config import CONFIG

config = CONFIG()

def init_db():
    print(f"[INIT] Using DB at: {config['SQL_ADDRESS']}")

    try:
        with DBCursor() as cur:
            result = initialize_database(cur)
            print(f"[INIT] Result: {result}")

    except Exception as e:
        print(f"[INIT] Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    init_db()