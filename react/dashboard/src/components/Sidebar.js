// src/components/Sidebar.js
import React from 'react';
import { NavLink } from 'react-router-dom';
import '../App.css';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="logo-container">
        <img src="/logo.png" alt="Logo" className="logo" />
      </div>
      <nav>
        <ul>
          <li>
            <NavLink to="/" activeClassName="active">Overview</NavLink>
          </li>
          <li>
            <NavLink to="/employee-data" activeClassName="active">Employee Data</NavLink>
          </li>
          <li>
            <NavLink to="/statistics" activeClassName="active">Statistics</NavLink>
          </li>
          <li>
            <NavLink to="/department-tree-view" activeClassName="active">Department Tree View</NavLink>
          </li>
          <li>
            <NavLink to="/interactive-map" activeClassName="active">Interactive Map</NavLink>
          </li>
          <li>
            <a href="https://streamlit.io/docs/" target="_blank" rel="noopener noreferrer">Streamlit Documentation</a>
          </li>
          <li>
            <a href="https://plotly.com/python/" target="_blank" rel="noopener noreferrer">Plotly Documentation</a>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;

