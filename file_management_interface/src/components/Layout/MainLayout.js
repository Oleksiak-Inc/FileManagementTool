import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import Sidebar from './Sidebar.js';
import { logout } from '../../services/auth.js';
import './MainLayout.css';

const MainLayout = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="main-layout">
            <Sidebar />
            <div className="main-content">
                <header className="main-header">
                    <div className="header-actions">
                        <button className="logout-btn" onClick={handleLogout}>
                            Logout
                        </button>
                    </div>
                </header>
                <main className="content-area">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default MainLayout;