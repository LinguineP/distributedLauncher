// ImageDisplay.js

import React, { useState, useEffect } from 'react';
import CommunicationHandler from '../../services/communicationHandler.ts';
import Modal from '../imageModal/imageModal.jsx';
import "./ImageDisplay.css";

function ImageDisplay({ imagePath }) {
    const [imageUrl, setImageUrl] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [modalOpen, setModalOpen] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            const communicationHandler = new CommunicationHandler();
            try {
                const url = await communicationHandler.fetchImage(imagePath);
                setImageUrl(url);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching image:', error);
                
                setError(error);
                setLoading(false);
            }
        };

        fetchData();
    }, [imagePath]);

    const openModal = () => {
        setModalOpen(true);
    };

    const closeModal = () => {
        setModalOpen(false);
    };

    if (loading) return <p>Loading...</p>;
    if (error) return <p>No image available</p>;

    return (
        <div className="image-container">
            <div onClick={openModal}>
                {imageUrl ? <img src={imageUrl} alt="Fetched from API" /> : <p>No image available</p>}
            </div>
            {modalOpen && <Modal imageUrl={imageUrl} onClose={closeModal} />}
        </div>
    );
}

export default ImageDisplay;
