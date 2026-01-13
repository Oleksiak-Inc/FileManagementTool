from sql_loader import SQL_COMMANDS

sql = SQL_COMMANDS()

def initialize_database(cur):
    try:
        cur.execute(sql["db"]["init"])
        return {
            "status": "success",
            "msg": "Database schema initialized successfully",
        }

    except Exception as e:
        return {
            "status": "fail",
            "msg": f"Cannot initialize database. Error: {e}",
        }
