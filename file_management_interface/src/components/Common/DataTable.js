import React from 'react';
import './DataTable.css';

const DataTable = ({ data, columns, onEdit, onDelete }) => {
    if (!data || data.length === 0) {
        return <div className="no-data">No data available</div>;
    }

    return (
        <table className="data-table">
            <thead>
                <tr>
                    {columns.map(col => (
                        <th key={col.key}>{col.title}</th>
                    ))}
                    {(onEdit || onDelete) && <th>Actions</th>}
                </tr>
            </thead>
            <tbody>
                {data.map((row, index) => (
                    <tr key={index}>
                        {columns.map(col => (
                            <td key={col.key}>
                                {col.render ? col.render(row[col.key], row) : row[col.key]}
                            </td>
                        ))}
                        {(onEdit || onDelete) && (
                            <td className="actions">
                                {onEdit && (
                                    <button 
                                        className="btn-edit"
                                        onClick={() => onEdit(row)}
                                    >
                                        Edit
                                    </button>
                                )}
                                {onDelete && (
                                    <button 
                                        className="btn-delete"
                                        onClick={() => onDelete(row.id)}
                                    >
                                        Delete
                                    </button>
                                )}
                            </td>
                        )}
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default DataTable;