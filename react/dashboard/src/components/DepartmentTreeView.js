// src/components/DepartmentTreeView.js
import React, { useState, useEffect } from 'react';
import TreeView from 'react-treeview';
import 'react-treeview/react-treeview.css';
import '../TreeView.css';
import Papa from 'papaparse';

const DepartmentTreeView = () => {
  const [treeData, setTreeData] = useState([]);

  useEffect(() => {
    Papa.parse('/data.csv', {
      download: true,
      header: true,
      complete: (results) => {
        const data = results.data;
        const departments = [...new Set(data.map(item => item.Department).filter(dept => dept))];  // Exclude empty departments
        const tree = departments.map(dept => {
          return {
            department: dept,
            collapsed: true,
            children: data.filter(item => item.Department === dept && item.Name).map((item) => ({
              name: item.Name,
            })),
          };
        });
        setTreeData(tree);
      }
    });
  }, []);

  const handleToggle = (index) => {
    const newTreeData = [...treeData];
    newTreeData[index].collapsed = !newTreeData[index].collapsed;
    setTreeData(newTreeData);
  };

  return (
    <div>
      <h1>Department Tree View</h1>
      <div className="tree-container">
        {treeData.map((node, index) => (
          <TreeView
            key={index}
            nodeLabel={<span onClick={() => handleToggle(index)} className="node-label">{node.department}</span>}
            collapsed={node.collapsed}
            itemClassName="tree-view_item"
            treeClassName="tree-view"
            arrowClassName={`tree-view_arrow ${node.collapsed ? 'collapsed' : ''}`}
          >
            {node.children.map((child, i) => (
              <div key={i} className="info">{child.name}</div>
            ))}
          </TreeView>
        ))}
      </div>
    </div>
  );
};

export default DepartmentTreeView;

