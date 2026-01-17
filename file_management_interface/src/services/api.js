import { getCookie } from '../utils/cookies.js';

const API_URL = 'http://localhost:5000/api/v1';

const getAuthHeaders = () => {
    const token = getCookie('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
    };
};

// Generic CRUD operations
export const fetchAll = async (endpoint) => {
    const response = await fetch(`${API_URL}/${endpoint}`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch');
    return response.json();
};

export const fetchById = async (endpoint, id) => {
    const response = await fetch(`${API_URL}/${endpoint}/${id}`, {
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch');
    return response.json();
};

export const create = async (endpoint, data) => {
    const response = await fetch(`${API_URL}/${endpoint}`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to create');
    return response.json();
};

export const update = async (endpoint, id, data) => {
    const response = await fetch(`${API_URL}/${endpoint}/${id}`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Failed to update');
    return response.json();
};

export const remove = async (endpoint, id) => {
    const response = await fetch(`${API_URL}/${endpoint}/${id}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to delete');
    return response.json();
};

// Specific entity endpoints
export const api = {
    // Auth
    login: (email, password) => fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    }).then(res => res.json()),

    // Entities
    resolutions: {
        getAll: () => fetchAll('resolutions'),
        create: (data) => create('resolutions', data)
    },
    scenarios: {
        getAll: () => fetchAll('scenarios'),
        create: (data) => create('scenarios', data)
    },
    statusSets: {
        getAll: () => fetchAll('status_sets'),
        create: (data) => create('status_sets', data)
    },
    testSuites: {
        getAll: () => fetchAll('test_suites'),
        create: (data) => create('test_suites', data)
    },
    statuses: {
        getAll: () => fetchAll('statuses'),
        create: (data) => create('statuses', data)
    },
    testCases: {
        getAll: () => fetchAll('test_cases'),
        create: (data) => create('test_cases', data)
    },
    testCaseVersions: {
        getAll: () => fetchAll('test_case_versions'),
        create: (data) => create('test_case_versions', data)
    },
    suitcases: {
        getAll: () => fetchAll('suitcases'),
        create: (data) => create('suitcases', data)
    },
    devices: {
        getAll: () => fetchAll('devices'),
        create: (data) => create('devices', data)
    },
    runs: {
        getAll: () => fetchAll('runs'),
        create: (data) => create('runs', data)
    },
    attachments: {
        getAll: () => fetchAll('attachments'),
        create: (data) => create('attachments', data)
    },
    executions: {
        getAll: () => fetchAll('executions'),
        create: (data) => create('executions', data),
        getByRun: (runId) => fetchById('executions/run', runId)
    },
    testers: {
        getCurrent: () => fetch(`${API_URL}/testers/me`, {
            headers: getAuthHeaders()
        }).then(res => res.json())
    }
};