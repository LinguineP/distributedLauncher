import React, { useState } from 'react';
import './expandableList.css'

const ExpandableList = () => {
  const items = [
    { id: 1, title: 'Item 1', content: 'Content for Item 1' },
    { id: 2, title: 'Item 2', content: 'Content for Item 2' },
    { id: 3, title: 'Item 3', content: 'Content for Item 3' },
  ];

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
        
        <div key={item.id} className="expandable-item">
          <div 
            onClick={() => toggleItem(item.id)} 
            className="expandable-header"
          >
            <span className="arrow">
              {expandedItems.includes(item.id) ? '▼' : '▶'}
            </span>
            <span className="title">
              {item.title}
            </span>
          </div>
          {expandedItems.includes(item.id) && (
            <div className="expandable-content">
              <p>{item.content}</p>
            </div>
          )}
        </div>
        
      ))}
    </div>
  );
};

export default ExpandableList;
