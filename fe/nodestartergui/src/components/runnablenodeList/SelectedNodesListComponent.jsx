import React, { useState, useRef,useEffect } from 'react';

const SelectedNodesList = ({ items, onItemClick, onItemLongPress,updateSelectedCount }) => {
  // eslint-disable-next-line no-unused-vars
  const [lastClickedItem, setLastClickedItem] = useState(null);
  const [lastLongPressedItem, setLastLongPressedItem] = useState(null);
  const [isLongPress, setIsLongPress] = useState(false);
  const pressTimer = useRef(null);

    useEffect(() => {
    updateSelectedCount(items.length);
  }, [items, updateSelectedCount]);

  const handleItemClick = (item) => {

    
    if (isLongPress) {
      setIsLongPress(false); // Reset long press flag
      return;
    }
    setLastClickedItem(item);
    onItemClick(item);
  };

  const handleLongPress = (item) => {
    setIsLongPress(true);
    setLastLongPressedItem(item); // Update the last long-pressed item
    onItemLongPress(item);
  };

  const handleMouseDown = (item) => {
    pressTimer.current = setTimeout(() => handleLongPress(item), 800); // 800ms for long press
  };

  const handleMouseUp = () => {
    clearTimeout(pressTimer.current);
  };

  const handleMouseLeave = () => {
    clearTimeout(pressTimer.current);
  };

  return (
    <ul>
      {items.map((item, index) => (
        <li
          key={index}
          onMouseDown={() => handleMouseDown(item)}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseLeave}
          onClick={() => handleItemClick(item)}
        >
          <strong>{item.hostname}</strong>: {item.ip}
          {lastLongPressedItem === item && <span className='Attention-text' id='masterStar'>★</span>}
        </li>
      ))}
    </ul>
  );
};

export default SelectedNodesList;
