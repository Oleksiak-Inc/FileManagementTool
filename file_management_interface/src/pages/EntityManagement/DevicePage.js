import React, { useEffect, useState } from 'react';
import { api } from '../../services/api.js';
import FormInput from '../../components/Common/FormInput.js';
import DataTable from '../../components/Common/DataTable.js';
import './EntityPage.css';

const DevicePage = () => {
    const [devices, setDevices] = useState([]);
    const [resolutions, setResolutions] = useState([]);
    const [form, setForm] = useState({ name: '', resolution_id: '' });

    useEffect(() => {
        api.devices.getAll().then(setDevices);
        api.resolutions.getAll().then(setResolutions);
    }, []);

    return (
        <div className="entity-page">
            <h1>Devices</h1>
            <form className="entity-form" onSubmit={async e => {
                e.preventDefault();
                await api.devices.create(form);
                setDevices(await api.devices.getAll());
            }}>
                <FormInput label="Name" value={form.name}
                    onChange={e => setForm({ ...form, name: e.target.value })} />
                <FormInput label="Resolution" type="select"
                    options={resolutions.map(r => ({
                        value: r.id,
                        label: `${r.w}x${r.h}`
                    }))}
                    onChange={e => setForm({ ...form, resolution_id: e.target.value })} />
                <button className="btn-primary">Create</button>
            </form>

            <DataTable data={devices}
                columns={[
                    { key: 'id', title: 'ID' },
                    { key: 'name', title: 'Name' },
                    { key: 'resolution_id', title: 'Resolution' }
                ]}
            />
        </div>
    );
};

export default DevicePage;
