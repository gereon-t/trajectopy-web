import React, { useState, useCallback, useRef } from 'react';
import { uploadFile } from '../api';
import './TrajectoryList.css';

const DetailRow = ({ label, value }) => (
    <div className="detail-row">
        <span className="detail-key">{label}:</span>
        <span className="detail-value">{value}</span>
    </div>
);

const TrajectoryList = ({
    sessionId,
    trajectories,
    onAddTrajectory,
    onToggleVisibility,
    onDelete,
    onCompare,
    isProcessing,
    onOpenSettings
}) => {

    const [selected, setSelected] = useState({ gt: null, est: null });
    const [dragOver, setDragOver] = useState(false);
    const [uploadError, setUploadError] = useState(null);
    const [loading, setLoading] = useState(false);

    const [expandedId, setExpandedId] = useState(null);

    const fileInputRef = useRef(null);

    const handleExpand = (id) => {
        setExpandedId(prevId => (prevId === id ? null : id));
    };

    const processFile = useCallback((file) => {
        if (!file) return;

        setLoading(true);
        setUploadError(null);

        uploadFile(file, sessionId)
            .then(response => {
                const fileData = {
                    name: response.name,
                    duration: response.duration,
                    datarate: response.datarate,
                    epsg: response.epsg,
                    num_poses: response.num_poses,
                    has_orientations: response.has_orientations,
                    session_id: response.session_id,
                    id: response.id,
                    positions: response.positions
                };
                onAddTrajectory(fileData);
            })
            .catch((err) => {
                console.error("Upload failed:", err);
                setUploadError(`Upload failed for ${file.name}.`);
            })
            .finally(() => {
                setLoading(false);
            });

    }, [sessionId, onAddTrajectory]);


    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragOver(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragOver(false);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragOver(true);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragOver(false);

        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            processFile(files[0]);
        }
    };

    const handleAddTrajectoryClick = () => {
        setUploadError(null);
        fileInputRef.current.click();
    };

    const handleFileInputChange = (e) => {
        const files = e.target.files;
        if (files && files.length > 0) {
            processFile(files[0]);
        }
        e.target.value = null;
    };


    const runCompare = () => {
        if (selected.gt && selected.est) {
            onCompare(selected.gt, selected.est);
        }
    };

    return (
        <div className='traj-list-wrapper'>
            <h3 className='traj-list-header'>Trajectories</h3>

            <button
                className='button add-traj-button'
                onClick={handleAddTrajectoryClick}
                disabled={loading || isProcessing}
            >
                {loading ? 'Processing...' : 'Add Trajectory'}
            </button>

            <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                onChange={handleFileInputChange}
                disabled={loading}
            />

            <div
                className={`traj-drop-zone ${dragOver ? 'active' : ''}`}
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
            >
                <p>...or drag a file here</p>
            </div>

            {uploadError && (
                <span className='upload-error'>{uploadError}</span>
            )}

            <div className='traj-list-items'>
                {trajectories.length === 0 && !loading && (
                    <span className='no-trajectories'>No trajectories added yet.</span>
                )}
                {loading && <div className='list-loading-spinner'><span>Loading...</span></div>}

                {trajectories.map(traj => {
                    const isExpanded = expandedId === traj.id;

                    // Helper function for clean data display
                    const formatValue = (value, fallback = 'N/A', processor) => {
                        if (value === undefined || value === null) return fallback;
                        if (processor) return processor(value);
                        return value;
                    };

                    return (
                        // A. New container for the whole item (header + details)
                        <div key={traj.id} className='traj-item-container'>

                            {/* B. The original 'traj-item' is now the header */}
                            <div className='traj-item-header' onClick={() => handleExpand(traj.id)}>
                                <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>▶</span>

                                <span title={traj.name} className='traj-item-name'>{traj.name}</span>

                                <div className='traj-item-actions'>
                                    {/* C. Stop propagation on all buttons */}
                                    <button
                                        onClick={(e) => { e.stopPropagation(); setSelected(s => ({ ...s, gt: traj.id })) }}
                                        className={`btn-select ${selected.gt === traj.id ? 'active' : ''}`}
                                        title="Set as Ground Truth"
                                    >GT</button>

                                    <button
                                        onClick={(e) => { e.stopPropagation(); setSelected(s => ({ ...s, est: traj.id })) }}
                                        className={`btn-select ${selected.est === traj.id ? 'active' : ''}`}
                                        title="Set as Estimated"
                                    >EST</button>

                                    <button
                                        onClick={(e) => { e.stopPropagation(); onToggleVisibility(traj.id) }}
                                        title={traj.isVisible ? "Hide on map" : "Show on map"}
                                    >{traj.isVisible ? '👁️' : '🚫'}</button>

                                    <button
                                        onClick={(e) => { e.stopPropagation(); onDelete(traj.id) }}
                                        title="Delete"
                                    >❌</button>
                                </div>
                            </div>

                            {/* D. Conditionally rendered details block */}
                            {isExpanded && (
                                <div className='traj-item-details'>
                                    <DetailRow label="Name" value={formatValue(traj.name)} />
                                    <DetailRow label="Number of Poses" value={formatValue(traj.num_poses)} />
                                    <DetailRow label="Duration" value={formatValue(traj.duration)} />
                                    <DetailRow label="Datarate [Hz]" value={formatValue(traj.datarate, 'N/A', val => val.toFixed(2))} />
                                    <DetailRow label="Has Orientations" value={formatValue(traj.has_orientations, 'N/A', val => val ? 'Yes' : 'No')} />
                                    <DetailRow label="EPSG" value={formatValue(traj.epsg)} />
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>


            <button className='button' onClick={onOpenSettings} disabled={isProcessing}>Settings</button>
            <button
                className='button compare-button'
                onClick={runCompare}
                disabled={
                    !selected.gt ||
                    !selected.est ||
                    selected.gt === selected.est ||
                    loading ||
                    isProcessing
                }
            >
                Compare (GT vs EST)
            </button>
        </div>
    );
};

export default TrajectoryList;