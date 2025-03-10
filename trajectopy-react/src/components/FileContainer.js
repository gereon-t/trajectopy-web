import React from 'react';
import './FileContainer.css';
import success from "../success.png";
import error from "../error.png";

const FileContainer = ({ fileInfo }) => {
    const fileStatusIcon = fileInfo.status === 'success' ? success : error;
    const trajectoryName = fileInfo.name === undefined ? 'N/A' : fileInfo.name;
    const epsg = fileInfo.epsg === undefined ? 'N/A' : fileInfo.epsg;
    const numberOfPoses = fileInfo.num_poses === undefined ? 'N/A' : fileInfo.num_poses;
    const hasOrientations = fileInfo.has_orientations === undefined ? 'N/A' : fileInfo.has_orientations === true ? 'Yes' : 'No';
    const duration = fileInfo.duration === undefined ? 'N/A' : fileInfo.duration;
    const datarate = fileInfo.datarate === undefined ? 'N/A' : fileInfo.datarate.toFixed(2);

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
                    <div className="file-info-name">Number of Poses:</div>
                    <div className="file-info-value">{numberOfPoses}</div>
                </div>

                <div className="file-info-row">
                    <div className="file-info-name">Duration:</div>
                    <div className="file-info-value">{duration}</div>
                </div>

                <div className="file-info-row">
                    <div className="file-info-name">Datarate [Hz]:</div>
                    <div className="file-info-value">{datarate}</div>
                </div>

                <div className="file-info-row">
                    <div className="file-info-name">Has Orientations:</div>
                    <div className="file-info-value">{hasOrientations}</div>
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