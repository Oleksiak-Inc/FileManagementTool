// src/pages/EntityManagement/ScenarioPage.js
import React, { useState, useEffect } from 'react';
import { api } from '../../services/api.js';
import FormInput from '../../components/Common/FormInput.js';
import DataTable from '../../components/Common/DataTable.js';
import './EntityPage.css';

const ScenarioPage = () => {
    const [scenarios, setScenarios] = useState([]);
    const [formData, setFormData] = useState({ name: '' });
    const [editingId, setEditingId] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchScenarios();
    }, []);

    const fetchScenarios = async () => {
        try {
            const data = await api.scenarios.getAll();
            setScenarios(data);
        } catch (error) {
            console.error('Failed to fetch scenarios:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editingId) {
                await api.update('scenarios', editingId, formData);
            } else {
                await api.scenarios.create(formData);
            }
            fetchScenarios();
            resetForm();
        } catch (error) {
            console.error('Failed to save scenario:', error);
        }
    };

    const handleEdit = (scenario) => {
        setFormData({ name: scenario.name });
        setEditingId(scenario.id);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this scenario?')) {
            try {
                await api.remove('scenarios', id);
                fetchScenarios();
            } catch (error) {
                console.error('Failed to delete scenario:', error);
            }
        }
    };

    const resetForm = () => {
        setFormData({ name: '' });
        setEditingId(null);
    };

    const columns = [
        { key: 'id', title: 'ID' },
        { key: 'name', title: 'Name' }
    ];

    if (loading) {
        return <div className="loading">Loading scenarios...</div>;
    }

    return (
        <div className="entity-page">
            <h1>Scenario Management</h1>
            
            <div className="entity-form">
                <h2>{editingId ? 'Edit Scenario' : 'Add New Scenario'}</h2>
                <form onSubmit={handleSubmit}>
                    <FormInput
                        label="Name"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="Enter scenario name"
                        required
                    />
                    <div className="form-actions">
                        <button type="submit" className="btn-primary">
                            {editingId ? 'Update' : 'Create'}
                        </button>
                        {editingId && (
                            <button type="button" className="btn-secondary" onClick={resetForm}>
                                Cancel
                            </button>
                        )}
                    </div>
                </form>
            </div>

            <div className="entity-list">
                <h2>Scenarios</h2>
                <DataTable
                    data={scenarios}
                    columns={columns}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                />
            </div>
        </div>
    );
};

export default ScenarioPage;