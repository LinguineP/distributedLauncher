import React, { useState } from 'react';

const AvailableScriptsList = ({ items, onItemClick }) => {
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
            style={{
              color: item === lastClickedItem ? 'red' : 'black',
              cursor: 'pointer',
            }}
          >
            <p list-text>{item}</p>
          </li>
        );
      
    })}
  </ul>
  );
};

export default AvailableScriptsList;
