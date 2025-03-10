import { plotTrajectory, ENDPOINT_URL } from '../api';
import React from 'react';

function renderReport(response) {
    const reportId = response.id;
    window.open(`${ENDPOINT_URL}/results/render/${reportId}`, '_blank');
}

const Plot = ({ sessionId, gtFileId, estFileId, settings, setLoading, loading }) => {

    const handleClick = () => {
        setLoading(true);
        const notNullIds = [gtFileId, estFileId].filter(id => id !== null);
        plotTrajectory(sessionId, notNullIds, settings).then(response => renderReport(response)).catch(error => {
            console.error('Failed to plot trajectories:', error);
        }).finally(() => setLoading(false))
    };

    const filesMissing = gtFileId === null && estFileId === null;

    return <button className='button' onClick={handleClick} disabled={loading || filesMissing}>Plot</button>
}

export default Plot;