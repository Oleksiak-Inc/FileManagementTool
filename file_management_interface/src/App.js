import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated } from './services/auth.js';
import MainLayout from './components/Layout/MainLayout.js';
import Login from './pages/Login.js';
import Dashboard from './pages/Dashboard.js';
import TestManagement from './pages/TestManagement/TestManagement.js';

// Entity Management Pages
import ResolutionPage from './pages/EntityManagement/ResolutionPage.js';
import ScenarioPage from './pages/EntityManagement/ScenarioPage.js';
import StatusSetPage from './pages/EntityManagement/StatusSetPage.js';
import TestSuitePage from './pages/EntityManagement/TestSuitePage.js';
import StatusPage from './pages/EntityManagement/StatusPage.js';
import TestCasePage from './pages/EntityManagement/TestCasePage.js';
import TestCaseVersionPage from './pages/EntityManagement/TestCaseVersionPage.js';
import SuitcasePage from './pages/EntityManagement/SuitcasePage.js';
import DevicePage from './pages/EntityManagement/DevicePage.js';
import RunPage from './pages/EntityManagement/RunPage.js';
import AttachmentPage from './pages/EntityManagement/AttachmentPage.js';
import ExecutionListPage from './pages/EntityManagement/ExecutionListPage.js';

// Execution Page
import ExecutionPage from './components/Execution/ExecutionPage.js';

import './App.css';

const PrivateRoute = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={
            <PrivateRoute>
              <MainLayout />
            </PrivateRoute>
          }>
            <Route index element={<Dashboard />} />
            <Route path="test-management" element={<TestManagement />} />
            
            {/* Entity Management Routes */}
            <Route path="resolutions" element={<ResolutionPage />} />
            <Route path="scenarios" element={<ScenarioPage />} />
            <Route path="status-sets" element={<StatusSetPage />} />
            <Route path="test-suites" element={<TestSuitePage />} />
            <Route path="statuses" element={<StatusPage />} />
            <Route path="test-cases" element={<TestCasePage />} />
            <Route path="test-case-versions" element={<TestCaseVersionPage />} />
            <Route path="suitcases" element={<SuitcasePage />} />
            <Route path="devices" element={<DevicePage />} />
            <Route path="runs" element={<RunPage />} />
            <Route path="attachments" element={<AttachmentPage />} />
            <Route path="executions" element={<ExecutionPage />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;