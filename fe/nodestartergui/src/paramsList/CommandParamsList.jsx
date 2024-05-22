import React, { useState } from 'react';
import './CommandParamsList.css'

const CommandParamsList = () => {
  const initialItems = [
    { id: 1, value: 'Item 1' },
    { id: 2, value: 'Item 2' },
    { id: 3, value: 'Item 3' },
  ];

  const [items, setItems] = useState(initialItems);
  const [editingItemId, setEditingItemId] = useState(null);
  const [tempValue, setTempValue] = useState('');
  const [newItemValue, setNewItemValue] = useState('');

  const handleEditClick = (id) => {
    if (editingItemId === id) {
      // Save changes
      setItems(items.map(item => (item.id === id ? { ...item, value: tempValue } : item)));
      setEditingItemId(null);
    } else {
      // Start editing
      const itemToEdit = items.find(item => item.id === id);
      setTempValue(itemToEdit.value);
      setEditingItemId(id);
    }
  };

  const handleInputChange = (e) => {
    setTempValue(e.target.value);
  };

  const handleDeleteOrCancelClick = (id) => {
    if (editingItemId === id) {
      // Cancel editing
      setEditingItemId(null);
    } else {
      // Delete item
      setItems(items.filter(item => item.id !== id));
    }
  };

  const handleAddItemClick = () => {
    if (newItemValue.trim() !== '') {
      const newId = Math.max(...items.map(item => item.id), 0) + 1;
      setItems([...items, { id: newId, value: newItemValue }]);
      setNewItemValue('');
    }
  };

  return (
    <div className="list-container">
      <div className="add-item-container">
        <input
          type="text"
          value={newItemValue}
          onChange={(e) => setNewItemValue(e.target.value)}
          placeholder="Type new params setting"
          className="list-input"
        />
        <button className="list-button add-button" onClick={handleAddItemClick}>Add</button>
      </div>
      <hr />
      <div className="list-container">
        {items.map(item => (
          <div className="list-item" key={item.id}>
            {editingItemId === item.id ? (
              <input
                type="text"
                value={tempValue}
                onChange={handleInputChange}
                className="list-input"
              />
            ) : (
              <span className="list-text">{item.value}</span>
            )}
            <button
              className="list-button edit-button"
              onClick={() => handleEditClick(item.id)}
            >
              {editingItemId === item.id ? 'Save Changes' : 'Edit'}
            </button>
            <button
              className={`list-button ${editingItemId === item.id ? 'cancel-button' : 'delete-button'}`}
              onClick={() => handleDeleteOrCancelClick(item.id)}
            >
              {editingItemId === item.id ? 'Cancel' : 'Delete'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};


export default CommandParamsList;
