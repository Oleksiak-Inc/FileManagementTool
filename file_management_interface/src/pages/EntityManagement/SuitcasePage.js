import React, { useEffect, useState } from 'react';
import { api } from '../../services/api.js';
import DataTable from '../../components/Common/DataTable.js';
import './EntityPage.css';

const SuitcasePage = () => {
    const [items, setItems] = useState([]);

    useEffect(() => {
        api.suitcases.getAll().then(setItems);
    }, []);

    return (
        <div className="entity-page">
            <h1>Suitcases</h1>
            <DataTable data={items}
                columns={[
                    { key: 'id', title: 'ID' },
                    { key: 'test_suite_id', title: 'Test Suite' },
                    { key: 'test_case_version_id', title: 'Test Case Version' }
                ]}
            />
        </div>
    );
};

export default SuitcasePage;
