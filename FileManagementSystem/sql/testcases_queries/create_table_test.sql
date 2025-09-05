CREATE TABLE IF NOT EXISTS test_cases_repository (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tc_scenario TEXT NOT NULL,
    tc_name TEXT NOT NULL,
    tc_description TEXT,
    tc_steps TEXT NOT NULL,
    tc_expected TEXT NOT NULL,
    statuses_list_id INTEGER NOT NULL,
    version TEXT,
    FOREIGN KEY (statuses_list_id) REFERENCES statuses_list(id),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS statuses_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    statuses JSON
);

CREATE TABLE IF NOT EXISTS test_suite_template (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    version TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS suitcase_map (
    suite_id INTEGER,
    case_id INTEGER,
    execution_order INTEGER DEFAULT 0,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (suite_id, case_id),
    FOREIGN KEY (suite_id) REFERENCES test_suite_template(id),
    FOREIGN KEY (case_id) REFERENCES test_cases_repository(id)
);

CREATE TABLE IF NOT EXISTS test_suite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_suite_template_id INTEGER,
    project_id INTEGER,
    suite_date DATE
);

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
    FOREIGN KEY(test_case_repo_id) REFERENCES test_cases_repo(id),
    FOREIGN KEY(test_suite_id) REFERENCES test_suite(id),
    FOREIGN KEY(path_id) REFERENCES file_list(id)
);