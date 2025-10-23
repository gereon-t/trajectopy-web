import React, { useState, useMemo } from 'react';
import TrajectoryList from './TrajectoryList';
import ResultList from './ResultList';
import MapView from './MapView';
import ErrorModal from './ErrorModal';
import SettingsModal from './SettingsModal';
import { defaultSettings } from '../settings';
import { deleteTrajectory, deleteReport, compareTrajectories, ENDPOINT_URL } from '../api';
import { colorCycle } from '../utils';
import './Base.css';


const Base = ({ sessionId, initialTrajectories, initialResults }) => {

    const [trajectories, setTrajectories] = useState(initialTrajectories);
    const [results, setResults] = useState(initialResults);

    const [isProcessing, setIsProcessing] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [errorVisible, setErrorVisible] = useState(false);
    const [isSettingsModalOpen, setIsSettingsModalOpen] = useState(false);
    const [currentSettings, setCurrentSettings] = useState(defaultSettings);

    const handleUpdateSettings = (settingName, value) => {
        setCurrentSettings(prevSettings => ({
            ...prevSettings,
            [settingName]: value,
        }));
    };

    const handleAddTrajectory = (fileData) => {
        const newColor = colorCycle[trajectories.length % colorCycle.length];

        const newTrajectory = {
            id: fileData.id,
            name: fileData.name,
            isVisible: true,
            positions: fileData.positions,
            epsg: fileData.epsg,
            num_poses: fileData.num_poses,
            duration: fileData.duration,
            datarate: fileData.datarate,
            has_orientations: fileData.has_orientations,
            color: newColor,
        };
        setTrajectories(prev => [...prev, newTrajectory]);
    };

    const handleToggleVisibility = (id) => {
        setTrajectories(prev =>
            prev.map(t =>
                t.id === id ? { ...t, isVisible: !t.isVisible } : t
            )
        );
    };

    const handleDeleteTrajectory = async (id) => {
        console.log("Deleting trajectory with id:", id);
        const trajToDelete = trajectories.find(t => t.id === id);
        if (!trajToDelete) return;

        try {
            await deleteTrajectory(trajToDelete.id);
            setTrajectories(prev => prev.filter(t => t.id !== id));
        } catch (error) {
            console.error("Failed to delete trajectory:", error.message);
            setErrorMessage(error.message);
            setErrorVisible(true);
        }
    };

    const handleDeleteResult = (id) => {
        console.log("Deleting result with id:", id);
        const resultToDelete = results.find(r => r.id === id);
        if (!resultToDelete) return;
        deleteReport(resultToDelete.id).catch(error => {
            console.error("Failed to delete result:", error.message);
            setErrorMessage(error.message);
            setErrorVisible(true);
        });
        setResults(prev => prev.filter(r => r.id !== id));
    };

    const handleClearResults = () => {
        results.forEach(result => {
            deleteReport(result.id).catch(error => {
                console.error("Failed to delete result:", error.message);
                setErrorMessage(error.message);
                setErrorVisible(true);
            });
        }
        );
        setResults([]);
    }

    const handleCompare = async (groundTruthId, estimatedId) => {
        const gt = trajectories.find(t => t.id === groundTruthId);
        const est = trajectories.find(t => t.id === estimatedId);

        if (!gt || !est) {
            console.error("Could not find trajectories to compare");
            return;
        }

        const gtFileId = gt.id;
        const estFileId = est.id;

        setIsProcessing(true);
        setErrorMessage('');
        setErrorVisible(false);

        try {
            const response = await compareTrajectories(sessionId, estFileId, gtFileId, currentSettings);

            const newResult = {
                id: response.id, // Use the report ID
                name: `${gt.name} vs ${est.name}`,
                reportUrl: `${ENDPOINT_URL}/results/render/${response.id}` // Store URL
            };
            setResults(prev => [newResult, ...prev]);

        } catch (error) {
            console.error('Failed to compare trajectories:', error);
            setErrorMessage(error.message);
            setErrorVisible(true);
        } finally {
            setIsProcessing(false);
        }
    };

    const visibleTrajectories = useMemo(() =>
        trajectories.filter(t => t.isVisible),
        [trajectories]
    );

    return (
        <div className='base-container-new'>
            <ErrorModal message={errorMessage} isOpen={errorVisible} onClose={() => setErrorVisible(false)} />
            <SettingsModal
                isOpen={isSettingsModalOpen}
                onUpdateSettings={handleUpdateSettings}
                onClose={() => setIsSettingsModalOpen(false)}
                settings={currentSettings}
            />
            <div className='left-panel'>
                <div className='trajectory-list-container'>
                    <TrajectoryList
                        sessionId={sessionId}
                        trajectories={trajectories}
                        onAddTrajectory={handleAddTrajectory}
                        onToggleVisibility={handleToggleVisibility}
                        onDelete={handleDeleteTrajectory}
                        onCompare={handleCompare}
                        isProcessing={isProcessing}
                        onOpenSettings={() => setIsSettingsModalOpen(true)}
                    />
                </div>
                <div className='result-list-container'>
                    <ResultList results={results} onDeleteResult={handleDeleteResult} onClearResults={handleClearResults} />
                </div>

            </div>
            <div className='right-panel'>
                <MapView trajectories={visibleTrajectories} />
            </div>
        </div>
    );
};

export default Base;