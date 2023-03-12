import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { useState } from 'react';

import Api from '../data';

import FileUpload from './FileUpload';


function Create() {
  const api = new Api();

  const [Submit, setSubmit] = useState(false);
  const [Queue, setQueue] = useState(0)

  const {
    acceptedFiles,
    fileRejections,
    getRootProps,
    getInputProps
  } = useDropzone({
    accept: {
      'audio/*': [],
    },
  });


  const acceptedFileItems = acceptedFiles.map((file, index) => (
    <li key={file.path}>
      <FileUpload index={index} file={file} submit={Submit} queue={Queue} setqueue={setQueue} />
    </li>
  ));


  const handleSubmit = () => {
    setSubmit(true)
    // console.log("waaa")
    // console.log(acceptedFiles)

    // for (const file of acceptedFiles) {
    //   data.append('files[]', file, file.name);
    // }

    // api.uploadFiles(acceptedFiles).then(response => {
    //   if (response.ok) {
    //     return response.json()
    //   }
    // }).then(prop => {
    //   console.log("check if success")
    //   console.log(prop)
    // }).catch(error => {
    //   console.error(error)
    // })

    // const data = new FormData();

    // data.append("audiofile", file, file.name)

    // axios({
    //   method: 'post',
    //   url: '/mediaresources/',
    //   responseType: 'json',
    //   data: null,
    //   headers: {
    //     'Content-Type': 'application/zip',
    //     'Content-Disposition': 'attachment; filename=' + "'" + acceptedFiles[0].name + "'",
    //     'Access-Control-Allow-Origin': '*',
    //     'X-CSRFTOKEN': document.querySelector('[name=csrfmiddlewaretoken]').value
    //   },
    //   onUploadProgress: function (progressEvent) {
    //     // var percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
    //     // setUploadProgress(percentCompleted)
    //     // console.log(percentCompleted);
    //   }
    // })
    //   .then(function (response) {

    //     if (response.status == 200) {

    //     }

    //   });

  }

  return (
    <section className="container">
      <div {...getRootProps({ className: 'dropzone' })}>
        <input {...getInputProps()} />
        <p>Drag 'n' drop some files here, or click to select files</p>
      </div>
      <aside>
        <h4>Accepted files</h4>
        <div>queue: {Queue}</div>
        <ul class="list-disc list-inside">{acceptedFileItems}</ul>
      </aside>
      <button onClick={handleSubmit}>send</button>
    </section>
  )
}

export default Create;