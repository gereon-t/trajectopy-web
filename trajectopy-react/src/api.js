export const ENDPOINT_URL = '';

export const createSession = async () => {
    const response = await fetch(ENDPOINT_URL + '/sessions/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (response.status !== 201) {
        const errorData = await response.json();
        throw new Error(errorData.message);
    }

    return response.json();
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

    return response.json();
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