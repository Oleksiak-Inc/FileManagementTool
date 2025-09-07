from sql_loader import SQL_COMMANDS

sql = SQL_COMMANDS()

def initialize_database(conn):
    try:
        conn.execute(sql['create_table_clients'])
        conn.execute(sql['create_table_projects'])
        conn.execute(sql['create_table_statuses_list'])
        conn.execute(sql['create_table_suitcase_map'])
        conn.execute(sql['create_table_test_cases_repository'])
        conn.execute(sql['create_table_test_cases_run'])
        conn.execute(sql['create_table_test_suite_template'])
        conn.execute(sql['create_table_test_suite'])
        conn.execute(sql['create_table_users'])
        conn.commit()
        return {"status": "success", "message": "Tables created successfully"}
    except Exception as e:
        return {"status": "fail", "message": f"Cannot create tables. Error: {e}"}
