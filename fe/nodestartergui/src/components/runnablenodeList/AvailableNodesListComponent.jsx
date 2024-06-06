import React, { useState } from 'react';

const AvailableNodesList = ({ items, onItemClick, }) => {
  // eslint-disable-next-line no-unused-vars
  const [lastClickedItem, setLastClickedItem] = useState(null);

  const handleItemClick = (item) => {
    setLastClickedItem(item);
    onItemClick(item);
  };

  return (
    <ul>
    {items.map((item, index) => {
        return (
          <li
            key={index}
            onClick={() => handleItemClick(item)}
          >
            <p list-text>{item.hostname}</p>: {item.ip}
          </li>
        );
    
    })}
  </ul>
  );
};

export default AvailableNodesList;
