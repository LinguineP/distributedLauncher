import React from 'react';
import "./imageModal.css";

const Modal = ({ imageUrl, onClose }) => {
    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content">
                <span className="close-button" onClick={onClose}>×</span>
                <img src={imageUrl} alt="Fetched from API" />
            </div>
        </div>
    );
};

export default Modal;
