import React, { useEffect, useState } from 'react';
import { api } from '../../services/api.js';
import FormInput from '../../components/Common/FormInput.js';
import DataTable from '../../components/Common/DataTable.js';
import './EntityPage.css';

const TestCaseVersionPage = () => {
    const [versions, setVersions] = useState([]);
    const [cases, setCases] = useState([]);
    const [form, setForm] = useState({ test_case_id: '', version: '', description: '' });

    useEffect(() => {
        api.testCaseVersions.getAll().then(setVersions);
        api.testCases.getAll().then(setCases);
    }, []);

    return (
        <div className="entity-page">
            <h1>Test Case Versions</h1>
            <form className="entity-form" onSubmit={async e => {
                e.preventDefault();
                await api.testCaseVersions.create(form);
                setVersions(await api.testCaseVersions.getAll());
            }}>
                <FormInput label="Test Case" type="select"
                    options={cases.map(c => ({ value: c.id, label: c.name }))}
                    onChange={e => setForm({ ...form, test_case_id: e.target.value })} />
                <FormInput label="Version" value={form.version}
                    onChange={e => setForm({ ...form, version: e.target.value })} />
                <FormInput label="Description" type="textarea"
                    value={form.description}
                    onChange={e => setForm({ ...form, description: e.target.value })} />
                <button className="btn-primary">Create</button>
            </form>

            <DataTable data={versions}
                columns={[
                    { key: 'id', title: 'ID' },
                    { key: 'test_case_id', title: 'Test Case' },
                    { key: 'version', title: 'Version' }
                ]}
            />
        </div>
    );
};

export default TestCaseVersionPage;
