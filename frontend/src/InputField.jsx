import React, { Fragment, useEffect, useState, useRef } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';


export default function InputField(props) {

    const [Textfieldhelperstate, setTextfieldhelperstate] = useState({ error: false, helperText: "", id: "outlined-error-helper-text" })
    // const [ValidatedUrl, setValidatedUrl] = useState('')
    const [DisableDownload, setDisableDownload] = useState(true)

    const ChangeURL = (value) => {
        // console.log(value.target.value)
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        var match = value.target.value.match(regExp);
        if (match && match[2].length == 11) {

            // console.log(match[2])
            setTextfieldhelperstate({ error: false, helperText: "" })
            setDisableDownload(false)
            props.setstatus('valid')
            props.seturl(match[2])

        } else {
            setTextfieldhelperstate({ error: true, helperText: "Incorrect URL" })
            props.setstatus('rejected')
            props.seturl('')
            setDisableDownload(true)
        }
    }

    return (
        <Fragment>
            <TextField
                {...Textfieldhelperstate}
                onChange={ChangeURL}
                onKeyPress={(e) => { e.key === 'Enter' && e.preventDefault(); }}
            />
            {/* <Button size="small" variant="contained" color="primary" disabled={!props.connect || DisableDownload}
                onClick={() => { props.url(ValidatedUrl) }}
            >
                Submit
            </Button> */}
        </Fragment >
    );
}

