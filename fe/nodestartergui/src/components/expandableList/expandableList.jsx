import React, { useState } from 'react';
import './expandableList.css'
import ImageDisplay from '../imageDisplay/ImageDisplay';

const ExpandableList = ({items}) => {
  

  const [expandedItems, setExpandedItems] = useState([]);

  const toggleItem = (id) => {
    setExpandedItems(prevState =>
      prevState.includes(id)
        ? prevState.filter(itemId => itemId !== id)
        : [...prevState, id]
    );
  };

  return (
    <div className="expandable-list">
      {items.map(item => (
        <div key={item.batch_id} className="expandable-item">
          <div onClick={() => toggleItem(item.batch_id)} className="expandable-header">
            <span className="arrow">
              {expandedItems.includes(item.batch_id) ? '▼' : '▶'}
            </span>
            <span className="title">
              {"batch id: "} {item.batch_id}{", batch params: "}{item.param_used}
            </span>
          </div>
          {expandedItems.includes(item.batch_id) && (
            <div className="expandable-content">
              <div className="table-container">
                <table className="table">
                  <tbody>
                    <tr>
                      <td>{"mean execution time: "}</td>
                      <td>{item.mean_execution_time}</td>
                    </tr>
                    <tr>
                      <td>{"standard deviation: "}</td>
                      <td>{item.standard_deviation}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <ImageDisplay imagePath={item.path_to_graph} />
            </div>
          )}
        </div>
      ))}
    </div>
  );

};

export default ExpandableList;
