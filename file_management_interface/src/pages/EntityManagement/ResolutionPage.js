import React, { useState, useEffect } from 'react';
import { api } from '../../services/api.js';
import FormInput from '../../components/Common/FormInput.js';
import DataTable from '../../components/Common/DataTable.js';
import './EntityPage.css';

const ResolutionPage = () => {
    const [resolutions, setResolutions] = useState([]);
    const [formData, setFormData] = useState({ w: '', h: '' });
    const [editingId, setEditingId] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchResolutions();
    }, []);

    const fetchResolutions = async () => {
        try {
            const data = await api.resolutions.getAll();
            setResolutions(data);
        } catch (error) {
            console.error('Failed to fetch resolutions:', error);
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
                await api.update('resolutions', editingId, formData);
            } else {
                await api.resolutions.create(formData);
            }
            fetchResolutions();
            resetForm();
        } catch (error) {
            console.error('Failed to save resolution:', error);
        }
    };

    const handleEdit = (resolution) => {
        setFormData({ w: resolution.w, h: resolution.h });
        setEditingId(resolution.id);
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this resolution?')) {
            try {
                await api.remove('resolutions', id);
                fetchResolutions();
            } catch (error) {
                console.error('Failed to delete resolution:', error);
            }
        }
    };

    const resetForm = () => {
        setFormData({ w: '', h: '' });
        setEditingId(null);
    };

    const columns = [
        { key: 'id', title: 'ID' },
        { key: 'w', title: 'Width' },
        { key: 'h', title: 'Height' }
    ];

    if (loading) {
        return <div className="loading">Loading resolutions...</div>;
    }

    return (
        <div className="entity-page">
            <h1>Resolution Management</h1>
            
            <div className="entity-form">
                <h2>{editingId ? 'Edit Resolution' : 'Add New Resolution'}</h2>
                <form onSubmit={handleSubmit}>
                    <FormInput
                        label="Width"
                        name="w"
                        type="number"
                        value={formData.w}
                        onChange={handleChange}
                        placeholder="Enter width"
                        required
                    />
                    <FormInput
                        label="Height"
                        name="h"
                        type="number"
                        value={formData.h}
                        onChange={handleChange}
                        placeholder="Enter height"
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
                <h2>Resolutions</h2>
                <DataTable
                    data={resolutions}
                    columns={columns}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                />
            </div>
        </div>
    );
};

export default ResolutionPage;