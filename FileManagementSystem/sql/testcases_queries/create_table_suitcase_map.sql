CREATE TABLE IF NOT EXISTS suitcase_map (
    suite_id INTEGER,
    case_id INTEGER,
    execution_order INTEGER DEFAULT 0,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (suite_id, case_id),
    FOREIGN KEY (suite_id) REFERENCES test_suite_template(id),
    FOREIGN KEY (case_id) REFERENCES test_cases_repository(id)
);