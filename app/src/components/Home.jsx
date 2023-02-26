import MediaResource from './MediaResource';
import React, { Fragment, useEffect, useState, useRef } from 'react';

import Api from '../data';

export default function Home() {
    const api = new Api();
    const [Data, setData] = useState(null);
    useEffect(() => {
        api.getMediaResourcesList().then(response => {
            if (response.ok) {
                return response.json()
            }
        }).then(prop => {
            setData(prop)
        }).catch(error => {
            // console.error(error)
        })
    }, [])

    function MediaList(props) {
        const listofmedia = props.listofmedia
        if (listofmedia == null) {
            return
        }
        const listItems = listofmedia.map((media, index) =>
            <li key={media.id}>
                {media.title}
            </li>
        );
        return (
            <ol class="list-decimal">
                {listItems}
            </ol>
        );
    }

    return (
        <div class="container mx-auto">
            <p><a href="accounts/logout/">Log Out</a></p>
            Index:
            <MediaList listofmedia={Data} />
        </div>
    );
}
