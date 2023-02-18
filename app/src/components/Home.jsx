import '../App.css';
import MediaResource from './MediaResource';
import React, { Fragment, useEffect, useState, useRef } from 'react';

import Api from '../data';

export default function Home() {
    const api = new Api();

    useEffect(() => {

        api.getMediaResourcesList(1).then(response => {
            if (response.ok) {
                return response.json()
            }
        }).then(prop => {
            console.log("heheh")
            console.log(prop)
        }).catch(error => {
            console.error(error)
        })
    }, [])


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
