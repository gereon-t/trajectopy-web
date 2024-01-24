import React from 'react';
import './FileContainer.css';
import success from "../success.png";
import error from "../error.png";

const FileContainer = ({ fileInfo }) => {
    const fileStatusIcon = fileInfo.status === 'success' ? success : error;
    const trajectoryName = fileInfo.name === undefined ? 'N/A' : fileInfo.name;
    const epsg = fileInfo.epsg === undefined ? 'N/A' : fileInfo.epsg;

    return <div className='file-container'>
        <div className='file-container-header'>

            <div className="file-name">File</div>
            <div className='file-symbols'>
                <img className='file-status-icon' src={fileStatusIcon} alt='status' />
                <div className="file-name">{fileInfo.fileName}</div>
            </div>
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