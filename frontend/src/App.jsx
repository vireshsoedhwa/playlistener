import React, { Fragment, useEffect, useState, useRef } from 'react';

import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import styles from './css/app.module.css';

// import List from '@material-ui/core/List';
// import ListItem from '@material-ui/core/ListItem';
// import ListItemText from '@material-ui/core/ListItemText';

import CircularProgressWithLabel from './CircularStatic';

// import InputField from './InputField';
import SubmitButton from './SubmitButton';
import Chooser from './Chooser';
import FileSubmit from './FileSubmit';
import UrlSubmit from './UrlSubmit';


export default function App() {
    const [Connect, setConnect] = useState(false);
    const [Url, setUrl] = useState('');
    const [Status, setStatus] = useState('idle');
    const [Received, setReceived] = useState('');
    const [Progress, setProgress] = useState(0);
    const [Submitclicked, setSubmitclicked] = useState(false);
    const [Mode, setMode] = useState(0)

    // const [Pollingdelay, setPollingdelay] = useState(null);
    /*
        status list:
        idle, valid, rejected , downloading , download_finished, finished, converting
    */
    // const ws = useRef(null);

    // const getId(url) {
    //     var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    //     var match = url.match(regExp);

    //     if (match && match[2].length == 11) {
    //         return match[2];
    //     } else {
    //         return 'error';
    //     }
    // }

    // useInterval(async () => {
    //     console.log("polling")
    //     if (!Connect) {
    //         makeConnection();
    //         console.log("retrying connection");
    //     }
    //     // setProgress((prevProgress) => (prevProgress >= 100 ? 0 : prevProgress + 10));
    // }, Pollingdelay);


    // useEffect(() => {
    //     console.log("initial connection")
    //     if (!Connect) {
    //         makeConnection();
    //         console.log("making connection")
    //         setPollingdelay(3000);
    //     }
    // }, [Connect]);

    // const makeConnection = () => {
    //     ws.current = new WebSocket(
    //         'ws://'
    //         + window.location.host
    //         + '/ws/'
    //     );

    //     ws.current.onopen = () => {
    //         console.log("ws opened");
    //         setConnect(true)
    //     }
    //     ws.current.onclose = (e) => {
    //         console.log("ws closed");
    //         console.error('socket closed unexpectedly ' + e);
    //         setConnect(false)

    //     }

    //     ws.current.onmessage = e => {
    //         const message = JSON.parse(e.data);
    //         setStatus(message.status)
    //         setReceived(message)
    //     };
    // }

    // useEffect(() => {
    //     if (Received.status === 'finished') {
    //         ws.current.close()
    //     }

    //     if (Received.status === 'submitted') {
    //         console.log('submitted')
    //         console.log(Status)
    //     }

    //     if (Received.status === 'downloading') {
    //         console.log('downloading')
    //         setProgress((Received.downloaded_bytes / Received.total_bytes) * 100)
    //     }

    //     if (Received.status === 'download_finished') {
    //         console.log('downloading finished')
    //         ws.current.close();
    //         setStatus('download_finished')
    //     }

    // }, [Received]);



    // const PostUrl = () => {
    //     const data = { url: Url };
    //     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    //     // console.log(csrftoken)
    //     let filename = "download.mp3";
    //     fetch('/api/submitlink', {
    //         method: 'POST', // or 'PUT'
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'Access-Control-Allow-Origin': '*',
    //             'X-CSRFTOKEN': csrftoken
    //         },
    //         body: JSON.stringify(data),
    //     })
    //         .then(response => {
    //             filename = response.headers.get('Content-Disposition').split('=')[1].slice(1, -1);
    //             return response.blob()
    //         })
    //         .then((blob) => {
    //             var a = document.createElement('a');
    //             a.href = window.URL.createObjectURL(blob);
    //             var attr = document.createAttribute("download");
    //             a.setAttributeNode(attr);
    //             a.style.display = 'none';
    //             a.download = filename;
    //             document.body.appendChild(a);
    //             a.click();
    //             a.remove();
    //         })
    //         .catch((error) => {
    //             console.error('Error:', error);
    //         });
    // }

    // useEffect(() => {
    //     if (Submitclicked && Connect) {
    //         console.log("Sending")
    //         ws.current.send(JSON.stringify({
    //             'request_type': 'submit',
    //             'url': Url
    //         }));
    //         // ws.current.close();
    //     }
    // }, [Submitclicked, Connect]);

    // const Submit = () => {
    //     // console.log(url)
    //     setSubmitclicked(true)
    //     makeConnection();
    // }

    // const QueryStatus = () => {
    //     ws.current.send(JSON.stringify({
    //         'request_type': 'polling',
    //         'url': Url
    //     }));
    // }

    return (
        <React.Fragment>
            <Container fixed>
                {/* <Stack spacing={2}> */}
                <Grid item xs container direction="column"
                    justifyContent="space-around"
                    alignItems="stretch"
                >
                    <Grid item xs>
                        <Chooser setmode={setMode} />
                    </Grid>
                    <Grid item>
                        {Mode == 1 ?
                            <FileSubmit></FileSubmit>
                            :
                            <UrlSubmit />
                        }
                    </Grid>
                    <Grid item xs>

                        list of RESULTs

                    </Grid>
                </Grid>
                {/* </Stack> */}
                {/* <InputField seturl={setUrl} connect={Connect} setstatus={setStatus} />
                {(Status === 'idle' || Status === 'rejected') ?
                    <div>

                    </div>
                    :
                    <div>
                        <div>
                            <img src={"//img.youtube.com/vi/" + Url + "/sddefault.jpg"} alt="youtube thumbnail" style={imgstyle} />
                        </div>
                    </div>
                }

                {Status === 'valid' ?
                    <div>
                        <SubmitButton submit={Submit} />
                    </div>
                    :
                    <div>

                    </div>
                }

                {Connect ?
                    <h2>
                        Connected
                    </h2>
                    :
                    <h2>
                        DIsconnecteed
                    </h2>
                }
                {Status}

                {Status === 'downloading' ?
                    <CircularProgressWithLabel value={Progress} />
                    :
                    <div>

                    </div>
                } */}


            </Container>
        </React.Fragment>
    );
}

// export function useInterval(callback, delay) {
//     const savedCallback = useRef();
//     //Remember the latest callback.
//     useEffect(() => {
//         savedCallback.current = callback;
//     }, [callback]);

//     //Set up the interval.
//     useEffect(() => {
//         function tick() {
//             savedCallback.current();
//         }
//         if (delay != null) {
//             const id = setInterval(tick, delay);
//             return () => {
//                 clearInterval(id);
//             };
//         }
//     }, [callback, delay]);
// }