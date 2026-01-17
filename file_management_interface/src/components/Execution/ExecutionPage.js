import React, { useState, useEffect } from 'react';
import { api } from '../../services/api.js';
import DataTable from '../Common/DataTable.js';
import './ExecutionPage.css';

const ExecutionPage = () => {
    const [executions, setExecutions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('all');

    useEffect(() => {
        fetchExecutions();
    }, []);

    const fetchExecutions = async () => {
        try {
            const data = await api.executions.getAll();
            setExecutions(data);
        } catch (error) {
            console.error('Failed to fetch executions:', error);
        } finally {
            setLoading(false);
        }
    };

    const filteredExecutions = executions.filter(execution => {
        if (filter === 'all') return true;
        if (filter === 'completed') return execution.status_id !== 4; // Assuming 4 is "Not Run"
        if (filter === 'pending') return execution.status_id === 4;
        return true;
    });

    const columns = [
        { key: 'id', title: 'ID' },
        { key: 'run_id', title: 'Run ID' },
        { key: 'test_case_version_id', title: 'Test Case Version' },
        { key: 'device_id', title: 'Device ID' },
        { key: 'status_id', title: 'Status ID' },
        { 
            key: 'executed_at', 
            title: 'Executed At',
            render: (value) => value ? new Date(value).toLocaleString() : 'Pending'
        },
        { key: 'execution_order', title: 'Order' }
    ];

    if (loading) {
        return <div className="loading">Loading executions...</div>;
    }

    return (
        <div className="execution-page">
            <div className="execution-header">
                <h1>Execution Management</h1>
                <div className="execution-filters">
                    <button 
                        className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
                        onClick={() => setFilter('all')}
                    >
                        All Executions
                    </button>
                    <button 
                        className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
                        onClick={() => setFilter('completed')}
                    >
                        Completed
                    </button>
                    <button 
                        className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
                        onClick={() => setFilter('pending')}
                    >
                        Pending
                    </button>
                </div>
            </div>

            <div className="execution-stats">
                <div className="stat-card">
                    <h3>Total Executions</h3>
                    <p className="stat-number">{executions.length}</p>
                </div>
                <div className="stat-card">
                    <h3>Completed</h3>
                    <p className="stat-number">{executions.filter(e => e.status_id !== 4).length}</p>
                </div>
                <div className="stat-card">
                    <h3>Pending</h3>
                    <p className="stat-number">{executions.filter(e => e.status_id === 4).length}</p>
                </div>
            </div>

            <div className="execution-list">
                <h2>Executions</h2>
                <DataTable
                    data={filteredExecutions}
                    columns={columns}
                />
            </div>
        </div>
    );
};

export default ExecutionPage;