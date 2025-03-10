import React from 'react';
import './Modal.css'


const ErrorModal = ({ message, isOpen, onClose }) => {
    return (
        isOpen && (
            <div className="modal">
                <div className="modal-content">
                    <div>Error: {message}</div>
                    <div className="modal-button-group">
                        <button className='modal-button' onClick={onClose}>Close</button>
                    </div>
                </div>
            </div>
        )
    );
};

export default ErrorModal;
