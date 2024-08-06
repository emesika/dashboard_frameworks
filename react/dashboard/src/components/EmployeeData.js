import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import '../App.css';

const EmployeeData = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [showRawData, setShowRawData] = useState(true);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: '' });

  useEffect(() => {
    Papa.parse('/data.csv', {
      download: true,
      header: true,
      complete: (results) => {
        setData(results.data);
        setFilteredData(results.data);
      },
    });
  }, []);

  useEffect(() => {
    let sortedData = [...data];
    if (selectedDepartment) {
      sortedData = sortedData.filter(row => row.Department === selectedDepartment);
    }
    if (searchTerm) {
      sortedData = sortedData.filter(row =>
        row.Name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    if (sortConfig.key !== null) {
      sortedData.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    setFilteredData(sortedData);
  }, [selectedDepartment, searchTerm, data, sortConfig]);

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    } else {
      direction = 'ascending';
    }
    setSortConfig({ key, direction });
  };

  const sortIndicator = (key) => {
    if (sortConfig.key !== key) return null;
    return (
        <span className="sort-indicator">
            {sortConfig.direction === 'ascending' ? '🔼' : '🔽'}
        </span>
    );
  };

  const departments = [...new Set(data.map(row => row.Department))];

  return (
    <div>
      <h1>Employee Data</h1>
      <select
        value={selectedDepartment}
        onChange={e => setSelectedDepartment(e.target.value)}
        style={{ width: '10%' }}
      >
        <option value="">Select Department</option>
        {departments.map(dept => (
          <option key={dept} value={dept}>{dept}</option>
        ))}
      </select>

      <input
        type="text"
        placeholder="Search by Name"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
        style={{ marginLeft: '10px' }}
      />

      <label style={{ marginLeft: '10px' }}>
        <input
          type="checkbox"
          checked={showRawData}
          onChange={e => setShowRawData(e.target.checked)}
        />
        Show Raw Data
      </label>

      <div className="table-container">
        <table className="custom-table">
          <thead>
            <tr>
              {data[0] && Object.keys(data[0]).map(key => (
                <th key={key} onClick={() => requestSort(key)} style={{ cursor: 'pointer' }}>
                  {key} <span className="sort-indicator">{sortIndicator(key)}</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredData.map((row, index) => (
              <tr key={index}>
                {Object.values(row).map((value, i) => <td key={i}>{value}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {showRawData && (
        <div className="table-container">
          <h2>Raw Data</h2>
          <table className="custom-table">
            <thead>
              <tr>
                {data[0] && Object.keys(data[0]).map(key => (
                  <th key={key} onClick={() => requestSort(key)} style={{ cursor: 'pointer' }}>
                    {key} <span className="sort-indicator">{sortIndicator(key)}</span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  {Object.values(row).map((value, i) => <td key={i}>{value}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default EmployeeData;

