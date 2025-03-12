import React from 'react';
import './SettingsModal.css';
import './Modal.css'


function capitalizeFirstLetter(settings_string) {
    const words = settings_string.split('_');

    for (let i = 0; i < words.length; i++) {

        if (words[i] === "ate") {
            words[i] = "ATE";
            continue;
        }

        if (words[i] === "rpe") {
            words[i] = "RPE";
            continue;
        }

        if (words[i] === "mm" || words[i] === "in") {
            continue;
        }

        words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
    }

    return words.join(' ');

}

const SettingsRow = ({ settingName, value, onUpdateSettings }) => {
    let inputElement;

    if (typeof value === 'boolean') {
        inputElement = <input type="checkbox" checked={value} onChange={e => onUpdateSettings(settingName, e.target.checked)} />;
    } else if (settingName === "matching") {
        inputElement = <select className='settings-input' value={value} onChange={(e) => onUpdateSettings(settingName, e.target.value)}>
            <option value="interpolation">Interpolation</option>
            <option value="nearest_temporal">Nearest Temporal</option>
            <option value="nearest_spatial">Nearest Spatial</option>
            <option value="nearest_spatial_interpolated">Nearest Spatial Interpolated</option>
        </select>
    } else if (settingName === "rpe_distance_unit") {
        inputElement = <select className='settings-input' value={value} onChange={(e) => onUpdateSettings(settingName, e.target.value)}>
            <option value="meter">Meter</option>
            <option value="second">Second</option>
        </select>
    }
    else {
        inputElement = <input className='settings-input'
            type="text"
            value={value}
            onChange={(e) => onUpdateSettings(settingName, e.target.value)}
        />
    }

    // Add tooltip for settings
    let tooltip;
    if (settingName === 'ate_in_mm') {
        tooltip = 'Absolute Trajectory Error in millimeters';

    } else if (settingName === 'directed_ate') {
        tooltip = 'Directed Absolute Trajectory Error in horizontal and vertical cross-track and along-track components';

    } else if (settingName === 'matching') {
        tooltip = 'Matching method for ground truth and estimated trajectories. Choices: interpolation, nearest temporal, nearest spatial, nearest spatial interpolated';

    } else if (settingName === 'similarity_transformation') {
        tooltip = 'Apply similarity transformation to estimated trajectory';

    } else if (settingName === 'estimate_scale') {
        tooltip = 'Estimate scale between ground truth and estimated trajectory';

    } else if (settingName === 'lever_arm_estimation') {
        tooltip = 'Estimate lever arm between ground truth and estimated trajectory';

    } else if (settingName === 'time_shift_estimation') {
        tooltip = 'Estimate time shift between ground truth and estimated trajectory';

    } else if (settingName === 'sensor_rotation_estimation') {
        tooltip = 'Estimate sensor rotation between ground truth and estimated trajectory';

    } else if (settingName === 'rpe_enabled') {
        tooltip = 'Relative Pose Error enabled';

    } else if (settingName === 'rpe_min_distance') {
        tooltip = 'Minimum distance for Relative Pose Error calculation';

    } else if (settingName === 'rpe_max_distance') {
        tooltip = 'Maximum distance for Relative Pose Error calculation';

    } else if (settingName === 'rpe_distance_step') {
        tooltip = 'Distance step for Relative Pose Error calculation';

    } else if (settingName === 'rpe_distance_unit') {
        tooltip = 'Distance unit for Relative Pose Error calculation. Choices: meter, second';

    } else if (settingName === 'rpe_use_all_pairs') {
        tooltip = 'Use all (overlapping) pairs for Relative Pose Error calculation';
    } else if (settingName === 'plot_on_map') {
        tooltip = 'Plot the trajectories on the map. Requires a georeferenced trajectory, internet connection and a mapbox access token for most map styles';
    } else if (settingName === 'map_style') {
        tooltip = 'Map style for plotting the trajectories. Choices: "basic", "carto-darkmatter", "carto-darkmatter-nolabels", "carto-positron", "carto-positron-nolabels", "carto-voyager", "carto-voyager-nolabels", "dark", "light", "open-street-map", "outdoors", "satellite", "satellite-streets", "streets", "white-bg"';
    }



    return <div key={settingName} className="setting-row">
        <label className='settings-label' title={tooltip}>{capitalizeFirstLetter(settingName)}</label>
        {inputElement}
    </div>
};

const SettingsModal = ({ isOpen, onUpdateSettings, onClose, settings }) => {
    return (
        isOpen && (
            <div className="modal">
                <div className="modal-content">
                    <div className='modal-title'>Settings</div>

                    <div className='modal-container'>
                        {Object.entries(settings).map(([settingName, value]) => (
                            <SettingsRow settingName={settingName} value={value} onUpdateSettings={onUpdateSettings} />
                        ))}
                    </div>
                    <div className="modal-button-group">
                        <button className='modal-button' onClick={onClose}>Close</button>
                    </div>
                </div>
            </div>
        )
    );
};

export default SettingsModal;
