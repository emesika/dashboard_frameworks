import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import '../App.css';

const EmployeeData = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [showRawData, setShowRawData] = useState(true);

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
    if (selectedDepartment) {
      setFilteredData(
        data.filter((row) => row.Department === selectedDepartment)
      );
    } else {
      setFilteredData(data);
    }
  }, [selectedDepartment, data]);

  useEffect(() => {
    if (searchTerm) {
      setFilteredData(
        data.filter((row) =>
          row.Name.toLowerCase().includes(searchTerm.toLowerCase())
        )
      );
    } else if (selectedDepartment) {
      setFilteredData(
        data.filter((row) => row.Department === selectedDepartment)
      );
    } else {
      setFilteredData(data);
    }
  }, [searchTerm, selectedDepartment, data]);

  const departments = [...new Set(data.map((row) => row.Department))];

  return (
    <div>
      <h1>Employee Data</h1>
      <select
        value={selectedDepartment}
        onChange={(e) => setSelectedDepartment(e.target.value)}
        style={{ width: '10%' }}
      >
        <option value="">Select Department</option>
        {departments.map((dept) => (
          <option key={dept} value={dept}>
            {dept}
          </option>
        ))}
      </select>

      <input
        type="text"
        placeholder="Search by Name"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{ marginLeft: '10px' }}
      />

      <label style={{ marginLeft: '10px' }}>
        <input
          type="checkbox"
          checked={showRawData}
          onChange={(e) => setShowRawData(e.target.checked)}
        />
        Show Raw Data
      </label>

      <div className="table-container">
        <table className="custom-table">
          <thead>
            <tr>
              {data[0] &&
                Object.keys(data[0]).map((key) => <th key={key}>{key}</th>)}
            </tr>
          </thead>
          <tbody>
            {filteredData.map((row, index) => (
              <tr key={index}>
                {Object.values(row).map((value, i) => (
                  <td key={i}>{value}</td>
                ))}
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
                {data[0] &&
                  Object.keys(data[0]).map((key) => <th key={key}>{key}</th>)}
              </tr>
            </thead>
            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  {Object.values(row).map((value, i) => (
                    <td key={i}>{value}</td>
                  ))}
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

