import React, { Fragment, useEffect, useState, useRef } from 'react';
// import { makeStyles } from '@material-ui/core/styles';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

// import List from '@material-ui/core/List';
// import ListItem from '@material-ui/core/ListItem';
// import ListItemText from '@material-ui/core/ListItemText';

import CircularProgressWithLabel from './CircularStatic';



export default function App() {
    const [Connect, setConnect] = useState(false);
    const [Url, setUrl] = useState('');
    const [Status, setStatus] = useState('idle');
    const [Polling, setPolling] = useState(false);
    const [Progress, setProgress] = useState(0);

    /*
        status list:
        idle, rejected , downloading , finished, converted
    */
    const ws = useRef(null);

    useInterval(async () => {
        if (!Connect) {
            makeConnection();
            console.log("making connection")
        }
        // setProgress((prevProgress) => (prevProgress >= 100 ? 0 : prevProgress + 10));
    }, 1000);


    // useEffect(() => {
    //     console.log("ayayayayay")
    //     if (!Connect) {
    //         makeConnection();
    //         console.log("making connection")
    //     }
    // }, [Connect]);

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
            setTimeout(function () {
                setConnect(false)
            }, 5000);

        }

        ws.current.onmessage = e => {
            const message = JSON.parse(e.data);

            setStatus(message.status)
            // if (message.status == 'submitted') {
            //     setPolling(true)
            // }

            // if (message.status == 'converted') {
            //     setPolling(false)
            // }

            // if (message.status == 'downloading') {
            //     let progress = (message.downloaded_bytes / message.total_bytes) * 100
            //     setProgress(progress)
            // }
            // if (message.status == 'finished' || message.status == 'converted') {
            //     setProgress(100)
            // }
            // if (message.status == 'converted') {
            //     setProgress(100)
            // }
            // console.log("e", e.data);
        };
    }

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

    const ChangeURL = (value) => {
        // console.log(value.target.value)
        setUrl(value.target.value)
    }

    const SubmitUrl = () => {
        ws.current.send(JSON.stringify({
            'request_type': 'submit',
            'url': Url
        }));
    }

    // const QueryStatus = () => {
    //     ws.current.send(JSON.stringify({
    //         'request_type': 'polling',
    //         'url': Url
    //     }));
    // }

    return (
        <React.Fragment>
            <Container maxWidth="sm">
                <Grid item xs={6}>
                    <form noValidate autoComplete="off">
                        <TextField id="standard-basic" label="Standard" onChange={ChangeURL} />
                        <Button size="small" variant="contained" color="primary"
                            onClick={SubmitUrl}
                        >
                            Submit
                        </Button>
                    </form>
                </Grid>
                <Grid item xs={6}>
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
                </Grid>
                <Grid item xs={6}>
                    {/* {Status} */}
                    <CircularProgressWithLabel value={Progress} />
                    {Status === 'converted' ?
                        <Button size="small" variant="contained" color="primary"
                            onClick={PostUrl}
                        >
                            Download
                        </Button>
                        :
                        <div>
                        </div>
                    }
                </Grid>
            </Container>
        </React.Fragment>
    );
}

export function useInterval(callback, delay) {
    const savedCallback = useRef();
    //Remember the latest callback.
    useEffect(() => {
        savedCallback.current = callback;
    }, [callback]);

    //Set up the interval.
    useEffect(() => {
        function tick() {
            savedCallback.current();
        }
        if (delay != null) {
            const id = setInterval(tick, delay);
            return () => {
                clearInterval(id);
            };
        }
    }, [callback, delay]);
}