import React, { useState, useEffect } from 'react';
import { api } from '../services/api.js';
import DataTable from '../components/Common/DataTable.js';
import './Dashboard.css';

const Dashboard = () => {
    const [runs, setRuns] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchRuns();
    }, []);

    const fetchRuns = async () => {
        try {
            const data = await api.runs.getAll();
            setRuns(data);
        } catch (error) {
            console.error('Failed to fetch runs:', error);
        } finally {
            setLoading(false);
        }
    };

    const columns = [
        { key: 'id', title: 'ID' },
        { key: 'name', title: 'Name' },
        { key: 'project_id', title: 'Project ID' },
        { 
            key: 'started_at', 
            title: 'Started At',
            render: (value) => value ? new Date(value).toLocaleString() : 'Not started'
        },
        { 
            key: 'done_at', 
            title: 'Completed At',
            render: (value) => value ? new Date(value).toLocaleString() : 'In progress'
        }
    ];

    if (loading) {
        return <div className="loading">Loading runs...</div>;
    }

    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <div className="dashboard-section">
                <h2>Recent Runs</h2>
                <DataTable data={runs.slice(0, 10)} columns={columns} />
            </div>
        </div>
    );
};

export default Dashboard;