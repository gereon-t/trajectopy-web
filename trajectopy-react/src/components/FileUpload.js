import React, { useState, useCallback } from 'react';
import './FileUpload.css';
import FileContainer from './FileContainer';
import { uploadFile } from '../api';

const FileUpload = ({ sessionId, setFileId }) => {
    const [dragOver, setDragOver] = useState(false);
    const [file, setFile] = useState(null);
    const [fileInfo, setFileInfo] = useState({});

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

        uploadFile(file, sessionId)
            .then(response => {
                setFileId(response.id);
                console.log('File uploaded:', response);
                setFileInfo({ fileName: file.name, epsg: response.epsg, name: response.name, status: 'success' });
            })
            .catch(() => {
                setFileInfo({ fileName: file.name, status: 'error' });
            });
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
                {dragOver ? <p>Drop the file here...</p> : <p>Click or drag a file here to upload</p>}
            </div>

            <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                onChange={handleFileInputChange}
            />
            {file && <FileContainer fileInfo={fileInfo} />}
        </div>
    );
}

export default FileUpload;
