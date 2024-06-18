import React from 'react';
import './ProgressBar.css';

const ProgressBar = ({ currentNumber, maxNumber }) => {
  const progress = (currentNumber / maxNumber) * 100;

  return (
    <div className="progress-bar-container">
      <div
        className="progress-bar"
        style={{ width: `${progress}%` }}
      >
        {Math.round(progress)}%
      </div>
    </div>
  );
};

export default ProgressBar;
