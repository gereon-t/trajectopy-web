import React, { useState } from 'react';
import FileUpload from './FileUpload';
import Compare from './Compare';
import './Base.css';
import Plot from './Plot';
import SettingsModal from './SettingsModal';
import { defaultSettings } from '../settings';

const Base = ({ sessionId }) => {

    const [gtFileId, setGtFileId] = useState(null);
    const [estFileId, setEstFileId] = useState(null);
    const [loading, setLoading] = useState(false);

    const [isSettingsModalOpen, setIsSettingsModalOpen] = useState(false);
    const [currentSettings, setCurrentSettings] = useState(defaultSettings);

    const handleUpdateSettings = (settingName, value) => {
        setCurrentSettings(prevSettings => ({
            ...prevSettings,
            [settingName]: value,
        }));
    };



    return (
        <div className='base-container'>
            <SettingsModal
                isOpen={isSettingsModalOpen}
                onUpdateSettings={handleUpdateSettings}
                onClose={() => setIsSettingsModalOpen(false)}
                settings={currentSettings}
            />
            <div className='content'>
                <div className='trajectories-container'>
                    <div className='trajectory-container'>
                        <div className='traj-title'>Ground Truth Trajectory</div>
                        <div className='traj-content'>
                            <FileUpload sessionId={sessionId} setFileId={setGtFileId} />
                        </div>
                    </div>
                    <div className='trajectory-divider' />
                    <div className='trajectory-container'>
                        <div className='traj-title'>Estimated Trajectory</div>
                        <div className='traj-content'>
                            <FileUpload sessionId={sessionId} setFileId={setEstFileId} />
                        </div>
                    </div>

                </div>
                <div className="button-row">
                    <button className='button' onClick={() => setIsSettingsModalOpen(true)}>Settings</button>
                    <div className='processing-button-row'>
                        {loading && <div className="loading-spinner" />}
                        < Plot sessionId={sessionId} gtFileId={gtFileId} estFileId={estFileId} settings={currentSettings} setLoading={setLoading} loading={loading} />
                        <div className='button-divider' />
                        < Compare sessionId={sessionId} gtFileId={gtFileId} estFileId={estFileId} settings={currentSettings} setLoading={setLoading} loading={loading} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Base;
