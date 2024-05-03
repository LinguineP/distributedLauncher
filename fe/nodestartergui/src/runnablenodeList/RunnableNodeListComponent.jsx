import React, { useState } from 'react';

const RunnableNodeList = ({ items, onItemClick }) => {
  const [lastClickedItem, setLastClickedItem] = useState(null);

  const handleItemClick = (item) => {
    setLastClickedItem(item);
    onItemClick(item);
  };

  return (
    <ul>
    {items.map((item, index,script) => {
      if (script) {
        return (
          <li
            key={index}
            onClick={() => handleItemClick(item)}
            style={{
              color: item === lastClickedItem ? 'red' : 'black',
              cursor: 'pointer',
            }}
          >
            <strong>{item}</strong>
          </li>
        );
      } else {
        return (
          <li
            key={index}
            onClick={() => handleItemClick(item)}
          >
            <strong>{item.hostName}</strong>: {item.ip}
          </li>
        );
      }
    })}
  </ul>
  );
};

export default RunnableNodeList;
