CREATE TABLE IF NOT EXISTS test_cases_run (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_case_repo_id INTEGER,
    test_suite_id INTEGER,
    path_id INTEGER,
    status_id INTEGER,
    tc_actual TEXT,
    issue JSON,
    comment JSON,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    executor_id INTEGER,
    FOREIGN KEY(test_case_repo_id) REFERENCES test_cases_repository(id),
    FOREIGN KEY(test_suite_id) REFERENCES test_suite(id),
    FOREIGN KEY(path_id) REFERENCES file_list(id)
);
