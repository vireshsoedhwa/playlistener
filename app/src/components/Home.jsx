import '../App.css';
import MediaResource from './MediaResource';
import React, { Fragment, useEffect, useState, useRef } from 'react';

import Api from '../data';

export default function Home() {
    const api = new Api();

    useEffect(() => {
        // console.log("waaa")
        // listupdate()
        let response = api
        .getMediaResourcesList()
        console.log("reposne")
        console.log(response)
    }, [])

    // const listupdate = () => {
    //     fetch('/mediaresources/', {
    //         method: 'get',
    //         mode: 'same-origin',
    //         credentials: 'same-origin',
    //         headers: {
    //             'Access-Control-Allow-Origin': '*',
    //             'Content-Type': 'application/json',
    //             'X-CSRFTOKEN': document.querySelector('[name=csrfmiddlewaretoken]').value
    //         },
    //         redirect: 'follow'
    //     })
    //         .then(response => {
    //             if (response.ok) {
    //                 console.log("")
    //                 return response.json()
    //             }
    //         })
    //         .then(data => {
    //             console.log(data)
    //         })
    //         .catch(error => {
    //             console.error(error)
    //         })
    // }

    // function MediaList(props) {
    //     const listofmedia = props.listofmedia
    //     if (listofmedia == null) {
    //         return
    //     }
    //     const listItems = listofmedia.map((media, index) =>
    //         <div key={media.id}>
    //             {props.filter != media.youtube_id ?
    //                 <YoutubeMediadetail data={media} listupdate={props.listupdate} delete_item={props.delete_item} retry={props.retry} archive={props.archive}/>
    //                 :
    //                 <div></div>
    //             }
    //         </div>
    //     );
    //     return (
    //         <Stack spacing={1}>{listItems}</Stack>
    //     );
    // }


    return (
        <div>
            <p><a href="accounts/logout/">Log Out</a></p>
            This is the home comp
        </div>
    );
}
