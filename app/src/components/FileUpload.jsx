import '../App.css';
import { useEffect, useState } from 'react';

import Api from '../data';

let FileUpload = (props) => {
  const [Done, setDone] = useState(false)
  const [Error, setError] = useState(null)
  const api = new Api();

  useEffect(() => {

    if (props.submit) {
      console.log("submit set")
      if (props.index == props.queue) {
        api.uploadFiles(props.file)
          .then((response) => {
            return response.json()
          })
          .then((value) => {
            setDone(true)
            props.setqueue(props.index + 1)
            try {
              setError(value['non_field_errors'][0])
            } catch {
              setError(null)
            }
          })
          .catch((error) => {
            console.log("something priblem")
            console.log(error)
          })
      }
    }
  }, [props.submit, props.queue])

  return (
    <span>
      <span className={`text-sm ${(Done) ?
        `${(Error) ?
          "text-red-800"
          :
          "text-green-800"
        }`
        : "text-blue-800"}`}>
        {props.file.name}
        {props.submit &&
          <>
            {Done ?
              <>
                {!Error &&
                  <span class="inline-flex items-baseline" >
                    <svg class="ml-1 mr-3 h-fit w-4 text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                      <circle class="opacity-40" cx="26" cy="26" r="25" fill="green" />
                      <path class="opacity-100" fill="green" d="M14.1 27.2l7.1 7.2 16.7-16.8" /></svg>
                  </span>
                }
              </>
              :
              <span class="inline-flex items-baseline" >
                <svg class="animate-spin ml-1 mr-3 h-fit w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="blue" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </span>
            }
          </>
        }
        {Error && <p className={`text-xs ${Error ? "text-red-700 italic" : ""}`}>
          {Error}
        </p>}
      </span>
      {/* <progress max="100" value="70" style={{ width: '100%', backgroundColor: 'red' }} /> */}
    </span>
  );
}

export default FileUpload
