import React, { useEffect, useState } from 'react';
import { api } from '../../services/api.js';
import FormInput from '../../components/Common/FormInput.js';
import DataTable from '../../components/Common/DataTable.js';
import './EntityPage.css';

const StatusPage = () => {
    const [statuses, setStatuses] = useState([]);
    const [sets, setSets] = useState([]);
    const [form, setForm] = useState({ name: '', status_set_id: '', is_final: false });

    useEffect(() => {
        api.statuses.getAll().then(setStatuses);
        api.statusSets.getAll().then(setSets);
    }, []);

    return (
        <div className="entity-page">
            <h1>Statuses</h1>
            <div className="entity-form">
                <form onSubmit={async e => {
                    e.preventDefault();
                    await api.statuses.create(form);
                    setForm({ name: '', status_set_id: '', is_final: false });
                    setStatuses(await api.statuses.getAll());
                }}>
                    <FormInput label="Name" value={form.name}
                        onChange={e => setForm({ ...form, name: e.target.value })} />
                    <FormInput label="Status Set" type="select"
                        value={form.status_set_id}
                        options={sets.map(s => ({ value: s.id, label: s.name }))}
                        onChange={e => setForm({ ...form, status_set_id: e.target.value })} />
                    <button className="btn-primary">Create</button>
                </form>
            </div>

            <DataTable data={statuses}
                columns={[
                    { key: 'id', title: 'ID' },
                    { key: 'name', title: 'Name' },
                    { key: 'status_set_id', title: 'Status Set' },
                    { key: 'is_final', title: 'Final' }
                ]}
            />
        </div>
    );
};

export default StatusPage;
