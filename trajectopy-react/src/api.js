export const ENDPOINT_URL = '';

export const createSession = async (name = null) => {
    let url = ENDPOINT_URL + '/sessions/create';

    if (name && name.trim() !== '') {
        url += `?name=${encodeURIComponent(name)}`;
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        let errorData;
        try {
            errorData = await response.json();
        } catch (e) {
            errorData = { message: 'Failed to create session. Unknown server error.' };
        }
        throw new Error(errorData.message || 'Failed to create session.');
    }

    return await response.json();
};

export const uploadFile = async (file, session_id) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(ENDPOINT_URL + '/trajectories/upload?' + new URLSearchParams({
        session_id: session_id,
    }), { method: 'POST', body: formData });

    if (response.status !== 201) {
        const errorData = await response.json();
        throw new Error(errorData.message);
    }

    const firstResponseData = await response.json();

    const trajectoryId = firstResponseData.id;
    const trajectoryResponse = await fetch(ENDPOINT_URL + `/trajectories/positions/${session_id}/${trajectoryId}`
        , {
            method: 'GET',
        });

    if (trajectoryResponse.status !== 200) {
        const errorData = await trajectoryResponse.json();
        throw new Error(errorData.message);
    }

    // merge both responses
    const trajectoryData = await trajectoryResponse.json();
    const mergedData = { ...firstResponseData, ...trajectoryData };

    return mergedData;
};


export const compareTrajectories = async (sessionId, estFileId, gtFileId, settings) => {
    const response = await fetch(ENDPOINT_URL + '/trajectories/compare?' + new URLSearchParams({
        session_id: sessionId, est_trajectory_id: estFileId, gt_trajectory_id: gtFileId
    }), {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(settings)
    });

    if (response.status !== 201) {
        const errorData = await response.json();
        throw new Error(errorData.message);
    }

    return response.json();
};

export const plotTrajectory = async (sessionId, trajectoryIds, settings) => {
    const response = await fetch(ENDPOINT_URL + '/trajectories/plot?' + new URLSearchParams({
        session_id: sessionId,
        plot_on_map: settings.plot_on_map,
        map_style: settings.map_style
    }), {
        method: 'POST', headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(trajectoryIds)
    });

    if (response.status !== 201) {
        const errorData = await response.json();
        throw new Error(errorData.message);
    }

    return response.json();
};

export const getReport = async (reportId) => {
    const response = await fetch(`${ENDPOINT_URL}/results/render/${reportId}`, { method: 'GET' });

    if (response.status !== 200) {
        const errorData = await response.json();
        throw new Error(errorData.message);
    }

    return response.json();
};

export const deleteTrajectory = async (trajectoryId) => {
    const response = await fetch(ENDPOINT_URL + `/trajectories/${trajectoryId}`, {
        method: 'DELETE',
    });
    if (response.status !== 204) {
        const errorData = await response.json();
        throw new Error(errorData.message);
    }
    return
};

export const deleteReport = async (reportId) => {
    const response = await fetch(ENDPOINT_URL + `/results/${reportId}`, {
        method: 'DELETE',
    });
    if (response.status !== 204) {
        const errorData = await response.json();
        throw new Error(errorData.message);
    }
    return
};

export const getSessions = async () => {
    const response = await fetch(ENDPOINT_URL + '/sessions/', {
        method: 'GET',
    });
    if (!response.ok) {
        throw new Error('Failed to fetch sessions.');
    }
    return await response.json();
};


export const getResults = async (sessionId) => {
    const response = await fetch(ENDPOINT_URL + `/results/?session_id=${sessionId}`, {
        method: 'GET',
    });
    if (!response.ok) {
        throw new Error('Failed to fetch results.');
    }
    return await response.json();
};


export const getTrajectoryPositions = async (sessionId, trajectoryId) => {
    const response = await fetch(ENDPOINT_URL + `/trajectories/positions/${sessionId}/${trajectoryId}`, {
        method: 'GET',
    });
    if (!response.ok) {
        throw new Error(`Failed to fetch positions for trajectory ${trajectoryId}.`);
    }
    return await response.json();
};

export const deleteSession = async (sessionId) => {
    const response = await fetch(ENDPOINT_URL + `/sessions/delete?session_id=${encodeURIComponent(sessionId)}`, {
        method: 'DELETE',
    });

    if (!response.ok) {
        let errorData;
        try {
            errorData = await response.json();
        } catch (e) {
            errorData = { message: 'Failed to delete session. Unknown server error.' };
        }
        throw new Error(errorData.message || 'Failed to delete session.');
    }
    return;
};