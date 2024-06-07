import React from 'react';
import './numberInput.css';

const NumberInput = ({ value, onChange, label }) => {


  const handleChange = (event) => {
    onChange(Number(event.target.value));
  };

  return (
    <div className="number-input">
      <p id='labelText'>{label}</p>
      <input
        type="number"
        value={value}
        onChange={handleChange}
      />
    </div>
  );
};

export default NumberInput;
