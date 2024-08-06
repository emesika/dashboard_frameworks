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
        const departments = [...new Set(data.map(item => item.Department).filter(dept => dept))];
        const tree = departments.map(dept => {
          return {
            name: dept,
            collapsed: true,
            children: data.filter(item => item.Department === dept).map((item) => ({
              name: item.Name,
              age: item.Age,
              city: item.City,
              collapsed: true,
              children: [
                { detail: `Age: ${item.Age}` },
                { detail: `City: ${item.City}` }
              ]
            })),
          };
        });
        setTreeData(tree);
      }
    });
  }, []);

  const handleToggle = (node) => {
    node.collapsed = !node.collapsed;
    setTreeData([...treeData]);
  };

  return (
    <div>
      <h1>Department Tree View</h1>
      <div className="tree-container">
        {treeData.map((node, index) => (
          <TreeView
            key={index}
            nodeLabel={<span onClick={() => handleToggle(node)} className="node-label">{node.name}</span>}
            collapsed={node.collapsed}
            itemClassName="tree-view_item"
            treeClassName="tree-view"
            arrowClassName={`tree-view_arrow ${node.collapsed ? 'collapsed' : ''}`}
          >
            {node.children.map((child, i) => (
              <TreeView
                key={i}
                nodeLabel={<span onClick={() => handleToggle(child)} className="node-label">{child.name}</span>}
                collapsed={child.collapsed}
                itemClassName="tree-view_item"
                treeClassName="tree-view"
                arrowClassName={`tree-view_arrow ${child.collapsed ? 'collapsed' : ''}`}
              >
                {child.children.map((detail, j) => (
                  <div key={j} className="info">{detail.detail}</div>
                ))}
              </TreeView>
            ))}
          </TreeView>
        ))}
      </div>
    </div>
  );
};

export default DepartmentTreeView;

