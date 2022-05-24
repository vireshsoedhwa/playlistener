import React, { Fragment, useEffect, useState, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import { css } from '@emotion/react';

export default function FileSubmit(props) {

    const { acceptedFiles, getRootProps, getInputProps } = useDropzone();

    const files = acceptedFiles.map(file => (
        <li key={file.path}>
            {file.path} - {file.size} bytes
        </li>
    ));


    return (
        <Fragment>
            <div {...getRootProps({ className: 'dropzone' })}>
                <input {...getInputProps()} />
                <p>Drag 'n' drop some files here, or click to select files</p>
            </div>
            <h4>Files</h4>
            <ul>{files}</ul>
        </Fragment >
    );
}

