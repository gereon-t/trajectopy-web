import React, { useState, useEffect } from 'react';
import { getSessions, deleteSession } from '../api';
import './SessionSelector.css';

const SessionSelector = ({ onCreateNew, onLoadOld, onError }) => {
    const [sessions, setSessions] = useState([]);
    const [loading, setLoading] = useState(true);

    const [sessionName, setSessionName] = useState('');

    useEffect(() => {
        const fetchSessions = async () => {
            try {
                const sessionData = await getSessions();
                // Sort sessions by date, newest first
                sessionData.sort((a, b) => new Date(b.date) - new Date(a.date));
                setSessions(sessionData);
            } catch (error) {
                onError(error.message);
            } finally {
                setLoading(false);
            }
        };
        fetchSessions();
    }, [onError]);

    const handleDeleteSession = async (e, sessionId) => {
        e.stopPropagation();

        if (!window.confirm("Are you sure you want to delete this session? This action cannot be undone.")) {
            return;
        }

        try {
            await deleteSession(sessionId);

            setSessions(prevSessions =>
                prevSessions.filter(session => session.id !== sessionId)
            );
        } catch (error) {
            onError(error.message);
        }
    };

    return (
        <div className="session-selector-container">
            <div className="session-box">
                <h2>Welcome to Trajectopy</h2>
                <p>Start a new session or load a previous one.</p>

                <input
                    type="text"
                    className="session-name-input"
                    placeholder="Optional: Name your new session"
                    value={sessionName}
                    onChange={(e) => setSessionName(e.target.value)}
                />

                <button
                    className="button new-session-btn"
                    onClick={() => onCreateNew(sessionName)}
                >
                    Start New Session
                </button>
            </div>

            <div className="session-box">
                <h3>Load Previous Session</h3>
                {loading && <div className="loading-spinner" />}
                {!loading && sessions.length === 0 && (
                    <p>No previous sessions found.</p>
                )}
                <div className="session-list">
                    {sessions.map(session => (
                        <button
                            key={session.id}
                            className="session-item"
                            onClick={() => onLoadOld(session)}
                        >
                            <div className="session-item-content">
                                <span className="session-name" title={session.id}>
                                    {session.name || `ID: ${session.id}`}
                                </span>
                                <span className="session-date">
                                    {new Date(session.date).toLocaleString()}
                                </span>
                            </div>

                            <button
                                className="session-delete-btn"
                                onClick={(e) => handleDeleteSession(e, session.id)}
                                title="Delete Session"
                            >
                                ❌
                            </button>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default SessionSelector;