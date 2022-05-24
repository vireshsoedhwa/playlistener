import React, { Fragment, useEffect, useState, useRef } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import { css } from '@emotion/react';
import Stack from '@mui/material/Stack';
import { createTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';

import CircularProgressWithLabel from './CircularStatic';

import FormControl from '@mui/material/FormControl';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputAdornment from '@mui/material/InputAdornment';
import InputLabel from '@mui/material/InputLabel';
import FormHelperText from '@mui/material/FormHelperText';

import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';


import ButtonBase from '@mui/material/ButtonBase';

import { styled } from '@mui/material/styles';

import LinearProgressWithLabel from './LinearWithLabel';

export default function UrlSubmit(props) {

    const [Textfieldhelperstate, setTextfieldhelperstate] = useState({ error: false, id: "outlined-error-helper-text" })
    const [DisableDownload, setDisableDownload] = useState(true)
    const [InputErrorMsg, setInputErrorMsg] = useState('')
    const [Valid, setValid] = useState(false)
    const [Url, setUrl] = useState('')
    const [Progress, setProgress] = useState(0)

    const [Connect, setConnect] = useState(false);
    const [Status, setStatus] = useState('idle');
    const [Received, setReceived] = useState('');
    const [Submitclicked, setSubmitclicked] = useState(false);
    const [Mode, setMode] = useState(0)

    const ws = useRef(null);

    const makeConnection = () => {
        ws.current = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/'
        );

        ws.current.onopen = () => {
            console.log("ws opened");
            setConnect(true)
        }
        ws.current.onclose = (e) => {
            console.log("ws closed");
            console.error('socket closed unexpectedly ' + e);
            setConnect(false)
        }

        ws.current.onmessage = e => {
            const message = JSON.parse(e.data);
            setStatus(message.status)
            setReceived(message)
        };
    }

    useEffect(() => {
        if (Received.status === 'finished') {
            ws.current.close()
        }

        if (Received.status === 'submitted') {
            console.log('submitted')
            console.log(Status)
        }

        if (Received.status === 'downloading') {
            console.log('downloading')
            setProgress((Received.downloaded_bytes / Received.total_bytes) * 100)
        }

        if (Received.status === 'download_finished') {
            console.log('downloading finished')
            ws.current.close();
            setStatus('download_finished')
        }

    }, [Received]);

    useEffect(() => {
        if (Submitclicked && Connect) {
            console.log("Sending")
            ws.current.send(JSON.stringify({
                'request_type': 'submit',
                'url': Url
            }));
            // ws.current.close();
        }
    }, [Submitclicked, Connect]);

    const Submit = () => {
        // console.log(url)
        setSubmitclicked(true)
        makeConnection();
    }

    const ChangeURL = (value) => {
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        var match = value.target.value.match(regExp);
        if (match && match[2].length == 11) {
            setTextfieldhelperstate({ error: false, helperText: "" })
            setTextfieldhelperstate({ error: false })
            setDisableDownload(false)
            setInputErrorMsg("")
            // props.setstatus('valid')
            // props.seturl(match[2])
            setUrl(match[2])
            setValid(true)
        } else {
            // setTextfieldhelperstate({ error: true, helperText: "Incorrect URL" })
            setTextfieldhelperstate({ error: true })
            setInputErrorMsg("Incorrect URL")
            // props.setstatus('rejected')
            // props.seturl('')
            setDisableDownload(true)
        }
    }

    const imgcontainer = {
        width: 'auto',
        height: 'auto',
        margin: '10px',
        border: 'solid 1px #CCC',
        backgroundColor: 'blue',
    }

    const settingsbox = {
        position: 'relative',
        width: 'auto',
        height: 'auto',
        margin: '20px',
        border: 'solid 1px #CCC',
        backgroundColor: '#090863',
        alignItems: 'center',
        justifyContent: 'center',
        display: 'block'
    }

    const Img = styled('img')({
        margin: 'auto',
        display: 'block',
        maxWidth: '100%',
        maxHeight: '100%',
    });

    return (
        <Fragment>
            <CssBaseline />
            <Paper
                sx={{
                    p: 2,
                    margin: 'auto',
                    maxWidth: '100%',
                    flexGrow: 1,
                    backgroundColor: (theme) =>
                        theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
                }}
            >

                <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
                    <Grid item xs={6}>


                        <Grid item xs container direction="column"
                            justifyContent="center"
                            alignItems="stretch"
                        >
                            <Grid item xs>
                                <FormControl fullWidth sx={{ m: 1 }}>
                                    <InputLabel htmlFor="outlined-adornment-amount">Youtube</InputLabel>
                                    <OutlinedInput
                                        // id="outlined-adornment-amount"
                                        id="component-error"
                                        // value=""
                                        onChange={ChangeURL}
                                        // error
                                        {...Textfieldhelperstate}
                                        startAdornment={<InputAdornment position="start">url:</InputAdornment>}
                                        label="Amount"
                                        aria-describedby="component-error-text"
                                    />
                                    <FormHelperText id="component-error-text">{InputErrorMsg}</FormHelperText>
                                </FormControl>
                            </Grid>
                            <Grid item xs>

                                <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>

                                    <Grid item xs={6}>
                                        <Box sx={{ p: 2, display: 'flex', justifyContent: 'center' }}>
                                            {Valid ?
                                                // <div>
                                                //     <img src={"//img.youtube.com/vi/" + Url + "/sddefault.jpg"} alt="youtube thumbnail" style={imgstyle} />
                                                // </div>
                                                <ButtonBase >
                                                    <Box sx={{ p: 2, border: '1px dashed grey' }}>
                                                        <Img alt="youtube" src={"//img.youtube.com/vi/" + Url + "/sddefault.jpg"} />
                                                    </Box>
                                                </ButtonBase>
                                                :
                                                <ButtonBase sx={{ width: 128, height: 128 }}>
                                                    <Box sx={{ p: 2 }}>
                                                    </Box>
                                                </ButtonBase>
                                            }
                                        </Box>

                                    </Grid>

                                    <Grid item xs={6}>

                                        {/* <CircularProgressWithLabel value={Progress} /> */}
                                        {Valid ?
                                            <>
                                                Download Progress
                                                <LinearProgressWithLabel value={Progress} />
                                                <Box sx={{ p: 2, display: 'flex', justifyContent: 'center' }}>
                                                    <Button
                                                        variant="contained"
                                                        onClick={Submit}
                                                    >Submit</Button>
                                                </Box>
                                            </>
                                            :
                                            <div>
                                            </div>
                                        }
                                    </Grid>





                                </Grid>




                            </Grid>
                        </Grid>


                    </Grid>


                    <Grid item xs={6}>
                        <Box sx={{ p: 2, border: '1px dashed grey', margin: 'auto' }}
                        >
                            <FormGroup>
                                <FormControlLabel control={<Checkbox defaultChecked />} label="Keep Video" />
                                <FormControlLabel control={<Checkbox />} label="Convert Audio to 432Hz" />
                            </FormGroup>
                        </Box>
                    </Grid>


                </Grid>
            </Paper>
        </Fragment >
    );
}
