
export const createSession = async () => {
    try {
        const response = await fetch('api/sessions/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.status !== 200) {
            throw new Error('Session creation failed');
        }

        return response.json();
    } catch (error) {
        console.error('Failed to start new session:', error);
    }
};

export const uploadFile = async (file, session_id) => {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('api/trajectories/upload?' + new URLSearchParams({
            session_id: session_id,
        }), { method: 'POST', body: formData });

        if (response.status !== 200) {
            throw new Error('Upload failed');
        }

        return response.json();

    } catch (error) {
        console.error('Failed to upload file:', error);
    }
};


export const compareTrajectories = async (sessionId, estFileId, gtFileId, settings) => {
    try {
        const response = await fetch('api/trajectories/compare?' + new URLSearchParams({
            session_id: sessionId, est_trajectory_id: estFileId, gt_trajectory_id: gtFileId
        }), {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(settings)
        });

        if (response.status !== 200) {
            throw new Error('Comparison failed');
        }

        return response.json();

    } catch (error) {
        console.error('Failed to compare trajectories:', error);
    }
};

export const plotTrajectory = async (sessionId, trajectoryIds) => {
    try {
        const response = await fetch('api/trajectories/plot?' + new URLSearchParams({
            session_id: sessionId
        }), {
            method: 'POST', headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(trajectoryIds)
        });

        if (response.status !== 200) {
            throw new Error('Plotting failed');
        }

        return response.json();

    } catch (error) {
        console.error('Failed to plot trajectories:', error);
    }
};

export const getReport = async (reportId) => {
    try {
        const response = await fetch(`api/results/render/${reportId}`, { method: 'GET' });

        if (response.status !== 200) {
            throw new Error('Failed to get report');
        }

        return response.json();

    } catch (error) {
        console.error('Failed to get report:', error);
    }
};