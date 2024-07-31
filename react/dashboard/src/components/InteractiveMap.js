// src/components/InteractiveMap.js
import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import Papa from 'papaparse';
import '../App.css';

const InteractiveMap = () => {
  const [data, setData] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState(null);

  useEffect(() => {
    Papa.parse('/data.csv', {
      download: true,
      header: true,
      complete: (results) => {
        const parsedData = results.data;
        const sortedData = parsedData.filter(row => row.Name && row.lat && row.lon).sort((a, b) => a.Name.localeCompare(b.Name));
        setData(sortedData);
        if (sortedData.length > 0) {
          setSelectedEmployee(sortedData[0]);
        }
      }
    });
  }, []);

  const handleEmployeeChange = (e) => {
    const employee = data.find(emp => emp.Name === e.target.value);
    setSelectedEmployee(employee);
  };

  if (data.length === 0) {
    return <div>Loading data...</div>;
  }

  return (
    <div>
      <h1>Interactive Map</h1>
      <p>This page displays an interactive map with employee locations.</p>
      <label htmlFor="employee-dropdown">Select an Employee:</label>
      <select id="employee-dropdown" onChange={handleEmployeeChange} value={selectedEmployee?.Name}>
        {data.map(employee => (
          <option key={employee.Name} value={employee.Name}>
            {employee.Name} ({employee.City})
          </option>
        ))}
      </select>
      <Plot
        data={[
          {
            type: 'scattermapbox',
            lat: data.map(employee => employee.lat),
            lon: data.map(employee => employee.lon),
            mode: 'markers',
            marker: { size: 9 },
            text: data.map(employee => `${employee.Name} (${employee.City})`)
          },
          ...(selectedEmployee ? [{
            type: 'scattermapbox',
            lat: [selectedEmployee.lat],
            lon: [selectedEmployee.lon],
            mode: 'markers+text',
            marker: { size: 12, color: 'red' },
            text: ['Selected Location'],
            textposition: 'top right'
          }] : [])
        ]}
        layout={{
          autosize: true,
          mapbox: {
            style: 'open-street-map',
            center: selectedEmployee ? {
              lat: selectedEmployee.lat,
              lon: selectedEmployee.lon
            } : {
              lat: data[0].lat,
              lon: data[0].lon
            },
            zoom: selectedEmployee ? 10 : 3
          },
          margin: { r: 0, t: 0, l: 0, b: 0 },
          showlegend: false
        }}
        style={{ width: '100%', height: '600px' }}
      />
    </div>
  );
};

export default InteractiveMap;

