import React, { useState, useEffect } from 'react';
import './DropdownMenuComponent.css';

const DropdownMenu = ({ placeholder, items, onSelectionChange, selectedItem, transformFunction }) => {
  const [localSelectedItem, setLocalSelectedItem] = useState('');

  useEffect(() => {
    setLocalSelectedItem(selectedItem);
  }, [selectedItem]);

  const handleChange = (event) => {
    const value = event.target.value;
    setLocalSelectedItem(value);
    onSelectionChange(value);
  };

  const transformedItems = transformFunction ? transformFunction(items) : items;

  return (
    <div className="dropdown-container">
      <select
        id="dropdown"
        className="dropdown-select"
        value={localSelectedItem}
        onChange={handleChange}
      >
        <option value="">{placeholder}</option>
        {transformedItems.map(item => (
          <option key={item.id} value={item.name}>
            {item.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default DropdownMenu;
