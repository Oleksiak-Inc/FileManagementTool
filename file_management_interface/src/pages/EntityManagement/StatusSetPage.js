import React, { useEffect, useState } from 'react';
import { api } from '../../services/api.js';
import FormInput from '../../components/Common/FormInput.js';
import DataTable from '../../components/Common/DataTable.js';
import './EntityPage.css';

const StatusSetPage = () => {
    const [items, setItems] = useState([]);
    const [formData, setFormData] = useState({ name: '' });
    const [editingId, setEditingId] = useState(null);

    const fetchData = async () => {
        setItems(await api.statusSets.getAll());
    };

    useEffect(() => { fetchData(); }, []);

    const submit = async e => {
        e.preventDefault();
        editingId
            ? await api.update('status_sets', editingId, formData)
            : await api.statusSets.create(formData);
        setFormData({ name: '' });
        setEditingId(null);
        fetchData();
    };

    return (
        <div className="entity-page">
            <h1>Status Sets</h1>
            <div className="entity-form">
                <form onSubmit={submit}>
                    <FormInput label="Name" value={formData.name}
                        onChange={e => setFormData({ name: e.target.value })} />
                    <button className="btn-primary">Save</button>
                </form>
            </div>
            <DataTable
                data={items}
                columns={[{ key: 'id', title: 'ID' }, { key: 'name', title: 'Name' }]}
                onEdit={r => { setFormData(r); setEditingId(r.id); }}
                onDelete={id => api.remove('status_sets', id).then(fetchData)}
            />
        </div>
    );
};

export default StatusSetPage;
