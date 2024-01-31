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
    } else {
        inputElement = <input className='settings-input'
            type="text"
            value={value}
            onChange={(e) => onUpdateSettings(settingName, e.target.value)}
        />
    }


    return <div key={settingName} className="setting-row">
        <label className='settings-label'>{capitalizeFirstLetter(settingName)}</label>
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
