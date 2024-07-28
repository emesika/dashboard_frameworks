// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Overview from './components/Overview';
import EmployeeData from './components/EmployeeData';
import Statistics from './components/Statistics';
import DepartmentTreeView from './components/DepartmentTreeView';
import InteractiveMap from './components/InteractiveMap';
import './App.css';

function App() {
  return (
    <div className="container">
      <Router>
        <Sidebar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/employee-data" element={<EmployeeData />} />
            <Route path="/statistics" element={<Statistics />} />
            <Route path="/department-tree-view" element={<DepartmentTreeView />} />
            <Route path="/interactive-map" element={<InteractiveMap />} />
            <Route path="*" element={<div>404 Page Not Found</div>} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;

