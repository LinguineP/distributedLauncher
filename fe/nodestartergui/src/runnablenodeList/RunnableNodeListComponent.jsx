import React from 'react';

const RunnableNodeList = ({ items,onItemClick }) => {
  return (
    <ul>
      {items.map((item,index) => (
        <li key={index} onClick={() => onItemClick(item)}>
          <strong>{item.hostName}</strong>: {item.ip}
        </li>
      ))}
    </ul>
  );
};

export default RunnableNodeList;