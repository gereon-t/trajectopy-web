import { compareTrajectories, ENDPOINT_URL } from '../api';
import React, { useState } from 'react';
import ErrorModal from './ErrorModal';

function renderReport(response) {
    const reportId = response.id;
    window.open(`${ENDPOINT_URL}/results/render/${reportId}`, '_blank');
}

const Compare = ({ sessionId, gtFileId, estFileId, settings, setLoading, loading }) => {
    const [errorMessage, setErrorMessage] = useState('');
    const [errorVisible, setErrorVisible] = useState(false);

    const handleClick = async () => {
        setLoading(true);
        try {
            const response = await compareTrajectories(sessionId, estFileId, gtFileId, settings);
            renderReport(response);
        } catch (error) {
            console.error('Failed to compare trajectories:', error);
            setErrorMessage(error.message);
            setErrorVisible(true);
        } finally {
            setLoading(false);
        }
    };

    const filesMissing = gtFileId === null || estFileId === null;

    return (
        <>
            <button className='button' onClick={handleClick} disabled={loading || filesMissing}>Compare</button>
            <ErrorModal message={errorMessage} isOpen={errorVisible} onClose={() => setErrorVisible(false)} />
        </>
    );
}

export default Compare;