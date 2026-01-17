import React, { useEffect, useState } from 'react';
import { api } from '../../services/api.js';
import FormInput from '../../components/Common/FormInput.js';
import DataTable from '../../components/Common/DataTable.js';
import './EntityPage.css';

const TestCasePage = () => {
    const [items, setItems] = useState([]);
    const [scenarios, setScenarios] = useState([]);
    const [form, setForm] = useState({ name: '', scenario_id: '' });

    useEffect(() => {
        api.testCases.getAll().then(setItems);
        api.scenarios.getAll().then(setScenarios);
    }, []);

    return (
        <div className="entity-page">
            <h1>Test Cases</h1>
            <form className="entity-form" onSubmit={async e => {
                e.preventDefault();
                await api.testCases.create(form);
                setItems(await api.testCases.getAll());
            }}>
                <FormInput label="Name" value={form.name}
                    onChange={e => setForm({ ...form, name: e.target.value })} />
                <FormInput label="Scenario" type="select"
                    options={scenarios.map(s => ({ value: s.id, label: s.name }))}
                    onChange={e => setForm({ ...form, scenario_id: e.target.value })} />
                <button className="btn-primary">Create</button>
            </form>

            <DataTable data={items}
                columns={[
                    { key: 'id', title: 'ID' },
                    { key: 'name', title: 'Name' },
                    { key: 'scenario_id', title: 'Scenario' }
                ]}
            />
        </div>
    );
};

export default TestCasePage;
