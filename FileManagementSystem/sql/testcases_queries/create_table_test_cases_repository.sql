CREATE TABLE IF NOT EXISTS test_cases_repository (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tc_scenario TEXT NOT NULL,
    tc_name TEXT NOT NULL,
    tc_description TEXT,
    tc_steps TEXT NOT NULL,
    tc_expected TEXT NOT NULL,
    statuses_list_id INTEGER NOT NULL,
    version TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (statuses_list_id) REFERENCES statuses_list(id)
);