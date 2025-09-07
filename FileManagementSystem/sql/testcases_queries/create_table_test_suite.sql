CREATE TABLE IF NOT EXISTS test_suite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_suite_template_id INTEGER,
    project_id INTEGER,
    suite_date DATE
);