import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
    const location = useLocation();

    const menuItems = [
        { path: '/', label: 'Dashboard', icon: '🏠' },
        { path: '/test-management', label: 'Test Management', icon: '🧪' },
        { path: '/resolutions', label: 'Resolutions', icon: '🖥️' },
        { path: '/scenarios', label: 'Scenarios', icon: '📋' },
        { path: '/status-sets', label: 'Status Sets', icon: '📊' },
        { path: '/statuses', label: 'Statuses', icon: '✅' },
        { path: '/test-suites', label: 'Test Suites', icon: '📁' },
        { path: '/test-cases', label: 'Test Cases', icon: '📝' },
        { path: '/test-case-versions', label: 'Test Case Versions', icon: '🔄' },
        { path: '/suitcases', label: 'Suitcases', icon: '🧳' },
        { path: '/devices', label: 'Devices', icon: '💻' },
        { path: '/runs', label: 'Runs', icon: '🏃' },
        { path: '/attachments', label: 'Attachments', icon: '📎' },
        { path: '/executions', label: 'Executions', icon: '⚡' },
    ];

    return (
        <div className="sidebar">
            <div className="sidebar-header">
                <h2>Test Management</h2>
            </div>
            <nav className="sidebar-nav">
                {menuItems.map(item => (
                    <Link
                        key={item.path}
                        to={item.path}
                        className={`sidebar-link ${location.pathname === item.path ? 'active' : ''}`}
                    >
                        <span className="sidebar-icon">{item.icon}</span>
                        <span className="sidebar-label">{item.label}</span>
                    </Link>
                ))}
            </nav>
        </div>
    );
};

export default Sidebar;