import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './TestManagement.css';

const TestManagement = () => {
    const [activeTab, setActiveTab] = useState('overview');

    const testGroups = [
        {
            title: 'Test Planning',
            items: [
                { to: '/scenarios', label: 'Scenarios', description: 'Manage test scenarios' },
                { to: '/test-suites', label: 'Test Suites', description: 'Organize test suites' },
                { to: '/test-cases', label: 'Test Cases', description: 'Create and manage test cases' },
            ]
        },
        {
            title: 'Configuration',
            items: [
                { to: '/resolutions', label: 'Resolutions', description: 'Configure screen resolutions' },
                { to: '/devices', label: 'Devices', description: 'Manage test devices' },
                { to: '/status-sets', label: 'Status Sets', description: 'Configure status categories' },
                { to: '/statuses', label: 'Statuses', description: 'Manage individual statuses' },
            ]
        },
        {
            title: 'Execution',
            items: [
                { to: '/runs', label: 'Runs', description: 'Manage test runs' },
                { to: '/executions', label: 'Executions', description: 'View and manage executions' },
                { to: '/suitcases', label: 'Suitcases', description: 'Link test cases to suites' },
            ]
        },
        {
            title: 'Versioning & Attachments',
            items: [
                { to: '/test-case-versions', label: 'Test Case Versions', description: 'Manage test case versions' },
                { to: '/attachments', label: 'Attachments', description: 'Manage test attachments' },
            ]
        }
    ];

    return (
        <div className="test-management">
            <h1>Test Management</h1>
            <p className="description">Central hub for managing all testing activities and configurations</p>
            
            <div className="test-groups">
                {testGroups.map((group, index) => (
                    <div key={index} className="test-group">
                        <h2>{group.title}</h2>
                        <div className="test-items">
                            {group.items.map((item, itemIndex) => (
                                <Link key={itemIndex} to={item.to} className="test-item">
                                    <h3>{item.label}</h3>
                                    <p>{item.description}</p>
                                </Link>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TestManagement;