import React, { Fragment, useEffect, useState, useRef } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';

import { alpha, styled } from '@mui/material/styles';
import { pink } from '@mui/material/colors';
import Switch from '@mui/material/Switch';

export default function Chooser(props) {

    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
        props.setmode(newValue)
    };

    return (
        <Fragment>
            {/* <Switch {...label} defaultChecked />
            <Switch {...label} defaultChecked color="secondary" />
            <Switch {...label} defaultChecked color="warning" />
            <Switch {...label} defaultChecked color="default" /> */}
            {/* <MaterialUISwitch {...label} defaultChecked /> */}
            <Tabs value={value} onChange={handleChange} centered>
                <Tab label="Youtube Url" />
                <Tab label="File" />
            </Tabs>
        </Fragment >
    );
}
