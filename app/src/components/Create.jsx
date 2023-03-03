import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

import Api from '../data';

function Create() {
  const api = new Api();

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


  const acceptedFileItems = acceptedFiles.map(file => (
    <li key={file.path}>
      {file.path} - {file.size} bytes
    </li>
  ));

  const handleSubmit = () => {
    // console.log("waaa")
    // console.log(acceptedFiles)

    // for (const file of acceptedFiles) {
    //   data.append('files[]', file, file.name);
    // }

    api.uploadFiles(acceptedFiles).then(response => {
      if (response.ok) {
        return response.json()
      }
    }).then(prop => {
      console.log("check if success")
      console.log(prop)
    }).catch(error => {
      console.error(error)
    })


  }

  return (
    <section className="container">
      <div {...getRootProps({ className: 'dropzone' })}>
        <input {...getInputProps()} />
        <p>Drag 'n' drop some files here, or click to select files</p>
      </div>
      <aside>
        <h4>Accepted files</h4>
        <ul>{acceptedFileItems}</ul>
      </aside>
      <button onClick={handleSubmit}>send</button>
    </section>
  )
}

export default Create;