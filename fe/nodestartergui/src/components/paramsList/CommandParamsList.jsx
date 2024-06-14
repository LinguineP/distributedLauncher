import React, { useState, useEffect } from 'react';
import '../../App.css'
import './CommandParamsList.css';
import CommunicationHandler from '../../services/communicationHandlers/communicationHandler.ts';

const CommandParamsList = ({ paramsList ,itemClicked} ) => {
    const [items, setItems] = useState([]);
    const [editingItemId, setEditingItemId] = useState(null);
    const [tempValue, setTempValue] = useState('');
    const [newItemValue, setNewItemValue] = useState('');
    const [lastClickedItemId, setLastClickedItemId] = useState(null); // Track last clicked item ID
    const requestHandler = new CommunicationHandler();

    useEffect(() => {
        setItems(paramsList);
    }, [paramsList]);

    const handleEditClick = async (id) => {
        if (editingItemId === id) {
            const updatedItem = { ...items.find(item => item.id === id), value: tempValue };
            try {
                await requestHandler.putCmdParam(id, updatedItem);
                setItems(items.map(item => (item.id === id ? updatedItem : item)));
                setEditingItemId(null);
                handleItemClick(id,updatedItem.value)
            } catch (error) {
                console.error('Error updating item:', error);
            }
        } else {
            const itemToEdit = items.find(item => item.id === id);
            setTempValue(itemToEdit.value);
            setEditingItemId(id);
        }
    };

    const handleInputChange = (e) => {
        setTempValue(e.target.value);
    };

    const handleDeleteOrCancelClick = async (id) => {
        if (editingItemId === id) {
            setEditingItemId(null);
        } else {
            try {
                await requestHandler.deleteCmdParam(id);
                setItems(items.filter(item => item.id !== id));
            } catch (error) {
                console.error('Error deleting item:', error);
            }
        }
    };

    const handleAddItemClick = async () => {
        if (newItemValue.trim() !== '') {
            const newId = Math.max(...items.map(item => item.id), 0) + 1;
            const newItem = { id: newId, value: newItemValue };

            try {
                const response = await requestHandler.postCmdParam(newItem);
                console.log("POST Response:", response);
                setItems([...items, newItem]);
                setNewItemValue('');
            } catch (error) {
                console.error("POST Error:", error);
            }
        }
    };

    const handleItemClick = (id, value) => {
        setLastClickedItemId(id); // Update last clicked item ID
        itemClicked(value); // Callback to parent with item text
    };

    return (
        <div className="list-container">
            <div className="add-item-container">
                        <p className="small-text Attention-text" id='ParamsFormat'>
                        Expected parameters format: numberOfNodes id (masternodeId) mip (application_specific_params)
                        </p>
                    <div className="add-item-input-row">
                        <input
                        type="text"
                        value={newItemValue}
                        onChange={(e) => setNewItemValue(e.target.value)}
                        placeholder="Example parameters: 2 id 0 mip"
                        className="list-input"
                        />
                        <button className="list-button add-button" onClick={handleAddItemClick}>Add</button>
                    </div>
        </div>
            <hr />
            <div className="list-container">
                {items.map(item => (
                    <div 
                        className={`list-item ${lastClickedItemId === item.id ? 'last-clicked' : ''}`} 
                        key={item.id} 
                        onClick={() => handleItemClick(item.id, item.value)}
                    >
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
