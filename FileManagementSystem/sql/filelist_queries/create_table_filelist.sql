CREATE TABLE IF NOT EXISTS file_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    project_id INTEGER,
    tester_id INTEGER,
    file_path TEXT,
    pc_no TEXT,
    resolution_id INTEGER,
    settings_id INTEGER,
    test_case_id INTEGER,
    status_id INTEGER,
    comment TEXT,
    meta JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key associations
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (tester_id) REFERENCES users(id)
    FOREIGN KEY (resolution_id) REFERENCES resolutions(id),
    FOREIGN KEY (settings_id) REFERENCES settings(id),
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id),
    FOREIGN KEY (status_id) REFERENCES statuses(id)
);