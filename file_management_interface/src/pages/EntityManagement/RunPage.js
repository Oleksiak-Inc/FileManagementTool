import React, { useEffect, useState } from 'react';
import { api } from '../../services/api.js';
import FormInput from '../../components/Common/FormInput.js';
import DataTable from '../../components/Common/DataTable.js';
import './EntityPage.css';

const RunPage = () => {
    const [runs, setRuns] = useState([]);
    const [suites, setSuites] = useState([]);
    const [form, setForm] = useState({ name: '', test_suite_id: '' });

    useEffect(() => {
        api.runs.getAll().then(setRuns);
        api.testSuites.getAll().then(setSuites);
    }, []);

    return (
        <div className="entity-page">
            <h1>Runs</h1>
            <form className="entity-form" onSubmit={async e => {
                e.preventDefault();
                await api.runs.create(form);
                setRuns(await api.runs.getAll());
            }}>
                <FormInput label="Name" value={form.name}
                    onChange={e => setForm({ ...form, name: e.target.value })} />
                <FormInput label="Test Suite" type="select"
                    options={suites.map(s => ({ value: s.id, label: s.name }))}
                    onChange={e => setForm({ ...form, test_suite_id: e.target.value })} />
                <button className="btn-primary">Create</button>
            </form>

            <DataTable data={runs}
                columns={[
                    { key: 'id', title: 'ID' },
                    { key: 'name', title: 'Name' },
                    { key: 'test_suite_id', title: 'Suite' }
                ]}
            />
        </div>
    );
};

export default RunPage;
