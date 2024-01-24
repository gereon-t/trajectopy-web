import React from 'react';
import './FileContainer.css';

const FileContainer = ({ fileInfo }) => {
    const fileStatusIcon = fileInfo.status === 'success' ? '✔' : '❌';
    const trajectoryName = fileInfo.name === undefined ? 'N/A' : fileInfo.name;
    const epsg = fileInfo.epsg === undefined ? 'N/A' : fileInfo.epsg;

    return <div className='file-container'>
        <div className='file-container-header'>
            <div className='file-symbols'>
                <div className="file-status">{fileStatusIcon}</div>
                <div className="file-icon">📄</div>
            </div>
            <div className="file-name">{fileInfo.fileName}</div>
        </div>

        <div className="file-info-container">
            <div className="file-details">
                <div className="file-info-row">
                    <div className="file-info-name">Name:</div>
                    <div className="file-info-value">{trajectoryName}</div>
                </div>

                <div className="file-info-row">
                    <div className="file-info-name">EPSG:</div>
                    <div className="file-info-value">{epsg}</div>
                </div>
            </div>

        </div>
    </div>

}

export default FileContainer;