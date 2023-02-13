import '../App.css';
import MediaResource from './MediaResource';
import React, { Fragment, useEffect, useState, useRef } from 'react';

export default function Home() {
    useEffect(() => {
        console.log("waaa")
        listupdate()
    }, [])

    const listupdate = () => {
        fetch('/mediaresources/', {
            method: 'get',
            mode: 'same-origin',
            credentials: 'same-origin',
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'X-CSRFTOKEN': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            redirect: 'follow'
        })
            .then(response => {
                if (response.ok) {
                    console.log("")
                    return response.json()
                }
                // throw response
            })
            .then(data => {
                console.log("")
                console.log(data)
            })
            .catch(error => {
                console.log("")
                console.error(error)
            })
    }


    return (
        <div>
            <p><a href="accounts/logout/">Log Out</a></p>
            This is the home comp
        </div>
    );
}
