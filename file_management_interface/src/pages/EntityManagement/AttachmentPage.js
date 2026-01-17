import React, { useEffect, useState } from 'react';
import { api } from '../../services/api.js';
import DataTable from '../../components/Common/DataTable.js';
import './EntityPage.css';

const AttachmentPage = () => {
    const [items, setItems] = useState([]);

    useEffect(() => {
        api.attachments.getAll().then(setItems);
    }, []);

    return (
        <div className="entity-page">
            <h1>Attachments</h1>
            <DataTable data={items}
                columns={[
                    { key: 'id', title: 'ID' },
                    { key: 'execution_id', title: 'Execution' },
                    { key: 'file_path', title: 'File Path' }
                ]}
            />
        </div>
    );
};

export default AttachmentPage;
