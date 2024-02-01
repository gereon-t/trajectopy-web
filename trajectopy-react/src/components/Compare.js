import { compareTrajectories, ENDPOINT_URL } from '../api';
import React from 'react';

function renderReport(response) {
    const reportId = response.id;
    window.open(`${ENDPOINT_URL}/results/render/${reportId}`, '_blank');
}

const Compare = ({ sessionId, gtFileId, estFileId, settings, setLoading, loading }) => {

    const handleClick = () => {
        setLoading(true);
        compareTrajectories(sessionId, estFileId, gtFileId, settings).then(response => renderReport(response)).catch(error => {
            console.error('Failed to compare trajectories:', error);
        }).finally(() => setLoading(false))
    };

    const filesMissing = gtFileId === null || estFileId === null;

    return <button className='button' onClick={handleClick} disabled={loading || filesMissing}>Compare</button>

}

export default Compare;