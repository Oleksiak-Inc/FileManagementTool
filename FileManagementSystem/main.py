import sqlite3 as sql
from app import create_app
from config import CONFIG
from app.services.db_init_service import initialize_database

config = CONFIG()
app = create_app()

def _init():
    print(f"[INIT] Using DB at: {config['SQL_ADDRESS']}")
    with sql.connect(config["SQL_ADDRESS"]) as conn:
        conn.row_factory = sql.Row
        result = initialize_database(conn)
        print(f"[INIT] Result: {result}")

        # Check if table 'users' exists
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"[INIT] Tables in DB: {tables}")

if __name__ == "__main__":
    _init()
    app.run(debug=True, host=config["HOST"], port=config["PORT"])
