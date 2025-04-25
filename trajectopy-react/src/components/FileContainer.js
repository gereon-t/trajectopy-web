import React from 'react';
import './FileContainer.css';
import success from "../success.png";
import error from "../error.png";

const FileContainer = ({ fileInfo, setFile }) => {
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
            <div className="file-symbols">
                <img className="file-status-icon" src={fileStatusIcon} alt="status" />
                <div className="file-name">{fileInfo.fileName}</div>
                <div className="trash-icon" onClick={() => setFile(null)}>
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 -6 20 28"
                        width="20"
                        height="20"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="icon-trash"
                    >
                        <polyline points="3 6 5 6 21 6" />
                        <path d="M19 6l-1 14H6L5 6" />
                        <path d="M10 11v6" />
                        <path d="M14 11v6" />
                        <path d="M9 6V4h6v2" />
                    </svg>
                </div>
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