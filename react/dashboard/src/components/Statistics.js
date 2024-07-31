import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';
import Papa from 'papaparse';
import '../App.css';

const Statistics = () => {
  const [data, setData] = useState([]);
  const [summaryStatistics, setSummaryStatistics] = useState([]);
  const [selectedStat, setSelectedStat] = useState('Mean');

  useEffect(() => {
    Papa.parse('/data.csv', {
      download: true,
      header: true,
      complete: (results) => {
        const parsedData = results.data;
        const filteredData = parsedData.filter(row => row.Department && row.Salary);
        setData(filteredData);

        const departments = Array.from(new Set(filteredData.map(row => row.Department)));
        const summaryStats = departments.map(dept => {
          const deptData = filteredData.filter(row => row.Department === dept);
          const salaries = deptData.map(row => parseFloat(row.Salary));
          const mean = salaries.reduce((a, b) => a + b, 0) / salaries.length;
          const median = salaries.sort((a, b) => a - b)[Math.floor(salaries.length / 2)];
          const sum = salaries.reduce((a, b) => a + b, 0);
          return { Department: dept, Mean: mean, Median: median, Sum: sum };
        });
        setSummaryStatistics(summaryStats);
      }
    });
  }, []);

  if (data.length === 0) {
    return <div>Loading data...</div>;
  }

  const salaryByDepartment = data.reduce((acc, row) => {
    if (!acc[row.Department]) {
      acc[row.Department] = 0;
    }
    acc[row.Department] += parseFloat(row.Salary);
    return acc;
  }, {});

  const departments = Object.keys(salaryByDepartment);
  const salaries = departments.map(dept => salaryByDepartment[dept]);

  const scatter3dData = departments.map(dept => {
    const deptData = data.filter(row => row.Department === dept);
    return {
      x: deptData.map(row => row.Department),
      y: deptData.map(row => parseFloat(row.Salary)),
      z: deptData.map(row => parseFloat(row.Age)),
      mode: 'markers',
      type: 'scatter3d',
      name: dept,
      marker: {
        size: 5,
        color: (() => {
          switch (dept) {
            case 'Finance': return 'blue';
            case 'HR': return 'lightblue';
            case 'Marketing': return 'red';
            case 'Engineering': return 'pink';
            default: return 'gray';
          }
        })()
      }
    };
  });

  const bins = [20, 30, 40, 50, 60];
  const labels = ["20-30", "30-40", "40-50", "50-60"];
  const ageIntervalData = data.map(row => {
    const age = parseInt(row.Age, 10);
    const interval = labels[bins.findIndex((bin, i) => age >= bin && age < bins[i + 1])];
    return { ...row, 'Age Interval': interval };
  });

  const ageIntervalByDepartment = departments.map(dept => {
    return {
      x: ageIntervalData.filter(row => row.Department === dept).map(row => row['Age Interval']),
      y: ageIntervalData.filter(row => row.Department === dept).map(row => parseFloat(row.Salary)),
      type: 'box',
      name: dept,
      boxpoints: 'all'
    };
  });

  const getSelectedSummaryStat = (stat) => {
    return summaryStatistics.map(deptStat => ({
      Department: deptStat.Department,
      Salary: deptStat[stat]
    }));
  };

  const selectedSummaryData = getSelectedSummaryStat(selectedStat);

  // Calculate detailed summary statistics for the table
  const detailedSummaryStats = data.reduce((acc, row) => {
    if (!acc[row.Department]) {
      acc[row.Department] = [];
    }
    acc[row.Department].push(parseFloat(row.Salary));
    return acc;
  }, {});

  const detailedSummaryData = Object.keys(detailedSummaryStats).map(dept => {
    const salaries = detailedSummaryStats[dept];
    const count = salaries.length;
    const mean = salaries.reduce((a, b) => a + b, 0) / count;
    const std = Math.sqrt(salaries.map(s => Math.pow(s - mean, 2)).reduce((a, b) => a + b) / count);
    const min = Math.min(...salaries);
    const max = Math.max(...salaries);
    const quartiles = [25, 50, 75].map(q => salaries.sort((a, b) => a - b)[Math.floor(q / 100 * count)]);
    return { Department: dept, Count: count, Mean: mean, Std: std, Min: min, '25%': quartiles[0], '50%': quartiles[1], '75%': quartiles[2], Max: max };
  });

  return (
    <div>
      <h1>Statistics</h1>
      <div>
        <h3>Salary Distribution</h3>
        <Plot
          data={departments.map(dept => ({
            x: [dept],
            y: [salaryByDepartment[dept]],
            type: 'bar',
            name: dept,
            marker: {
              color: (() => {
                switch (dept) {
                  case 'Finance': return 'blue';
                  case 'HR': return 'lightblue';
                  case 'Marketing': return 'red';
                  case 'Engineering': return 'pink';
                  default: return 'gray';
                }
              })()
            }
          }))}
          layout={{
            title: 'Salary Distribution by Department',
            barmode: 'group',
            showlegend: true,
            legend: {
              x: 1,
              y: 1
            },
            width: 1500 // Add this line to set the width
          }}
        />
      </div>
      <div>
        <h3>3D Salary Distribution</h3>
        <Plot
          data={scatter3dData}
          layout={{
            title: '3D Salary Distribution by Department and Age',
            showlegend: true,
            legend: {
              x: 1,
              y: 1
            },
            width: 1500 // Add this line to set the width
          }}
        />
      </div>
      <div>
        <h3>Salary by Age Intervals Cross Departments</h3>
        <Plot
          data={ageIntervalByDepartment}
          layout={{
            title: 'Salary by Age Intervals Cross Departments',
            xaxis: {
              title: 'Age Interval',
              categoryorder: 'array',
              categoryarray: labels
            },
            yaxis: { title: 'Salary' },
            boxmode: 'group',
            showlegend: true,
            legend: {
              x: 1,
              y: 1
            },
            width: 1500 // Add this line to set the width
          }}
        />
      </div>
      <div>
        <h3>Summary Statistics</h3>
        <table className="custom-table">
          <thead>
            <tr>
              <th>Department</th>
              <th>Count</th>
              <th>Mean</th>
              <th>Std</th>
              <th>Min</th>
              <th>25%</th>
              <th>50%</th>
              <th>75%</th>
              <th>Max</th>
            </tr>
          </thead>
          <tbody>
            {detailedSummaryData.map(stat => (
              <tr key={stat.Department}>
                <td>{stat.Department}</td>
                <td>{stat.Count}</td>
                <td>{stat.Mean.toFixed(2)}</td>
                <td>{stat.Std.toFixed(2)}</td>
                <td>{stat.Min}</td>
                <td>{stat['25%']}</td>
                <td>{stat['50%']}</td>
                <td>{stat['75%']}</td>
                <td>{stat.Max}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div>
          <input
            type="radio"
            value="Mean"
            checked={selectedStat === 'Mean'}
            onChange={() => setSelectedStat('Mean')}
          /> Mean
          <input
            type="radio"
            value="Median"
            checked={selectedStat === 'Median'}
            onChange={() => setSelectedStat('Median')}
          /> Median
          <input
            type="radio"
            value="Sum"
            checked={selectedStat === 'Sum'}
            onChange={() => setSelectedStat('Sum')}
          /> Sum
        </div>
        <table className="custom-table">
          <thead>
            <tr>
              <th>Department</th>
              <th>{selectedStat}</th>
            </tr>
          </thead>
          <tbody>
            {selectedSummaryData.map(stat => (
              <tr key={stat.Department}>
                <td>{stat.Department}</td>
                <td>{stat.Salary.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Statistics;

