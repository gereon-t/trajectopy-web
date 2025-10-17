import React, { useState, useCallback } from 'react';
import './FileUpload.css';
import FileContainer from './FileContainer';
import { uploadFile } from '../api';

const FileUpload = ({ sessionId, setFileId }) => {
    const [dragOver, setDragOver] = useState(false);
    const [file, setFile] = useState(null);
    const [fileInfo, setFileInfo] = useState({});

    const [loading, setLoading] = useState(false);

    const handleDragEnter = e => {
        e.preventDefault();
        e.stopPropagation();
        setDragOver(true);
    };

    const handleDragLeave = e => {
        e.preventDefault();
        e.stopPropagation();
        setDragOver(false);
    };

    const handleDragOver = e => {
        e.preventDefault();
        e.stopPropagation();
        setDragOver(true);
    };

    const handleDrop = e => {
        e.preventDefault();
        e.stopPropagation();
        setDragOver(false);

        const files = e.dataTransfer.files;
        if (files && files.length > 0) {
            const file = files[0];
            setFile(file);
            processFile(file);
        }
    };


    const processFile = useCallback((file) => {
        console.log('Processing file:', file.name);
        setLoading(true);

        uploadFile(file, sessionId)
            .then(response => {
                setFileId(response.id);
                console.log('File uploaded:', response);
                setFileInfo({ fileName: file.name, epsg: response.epsg, num_poses: response.num_poses, has_orientations: response.has_orientations, name: response.name, duration: response.duration, datarate: response.datarate, status: 'success' });
            })
            .catch(() => {
                setFileInfo({ fileName: file.name, status: 'error' });
            }).finally(() => setLoading(false));
    }, [sessionId, setFileId]);

    const handleUploadAreaClick = () => {
        if (fileInputRef.current) {
            fileInputRef.current.click();
        }
    };

    const handleFileInputChange = (e) => {
        const files = e.target.files;
        if (files && files.length > 0) {
            const file = files[0];
            setFile(file);
            processFile(file);
        }
    };

    React.useEffect(() => {
        if (file === null) {
            setFileId(null);
            setFileInfo({});
        }
    }, [file, setFileId]);

    const fileInputRef = React.createRef();

    return (
        <div>
            <div
                className={`drop-zone ${dragOver ? 'active' : ''}`}
                onClick={handleUploadAreaClick}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
            >
                {dragOver ? <p className='drop-message'>Drop the file here...</p> : <p className='drop-message'>Click or drag a file here to upload</p>}
            </div>

            <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                onChange={handleFileInputChange}
            />
            {loading ? <div className="file-loading-spinner" /> : file && <FileContainer fileInfo={fileInfo} setFile={setFile} />}
        </div>
    );
}

export default FileUpload;
