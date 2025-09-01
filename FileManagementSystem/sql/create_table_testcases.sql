CREATE TABLE test_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    suite_id INTEGER,
    key TEXT,
    value TEXT,
    FOREIGN KEY(suite_id) REFERENCES test_suites(id)
);