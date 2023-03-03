export default class Api {

    constructor() {
        // this.api_token = null;
        this.client = null;
        this.api_url = process.env.REACT_APP_API_ENDPOINT;
        this.headers = new Headers();
        this.headers.append("X-CSRFTOKEN", document.querySelector('[name=csrfmiddlewaretoken]').value)
        this.headers.append("Access-Control-Allow-Origin", "*")

    }

    init = (params) => {
        // this.api_token = getCookie("ACCESS_TOKEN");

        // let headers = {
        //     'Access-Control-Allow-Origin': '*',
        //     'Content-Type': 'application/json',
        //     'X-CSRFTOKEN': document.querySelector('[name=csrfmiddlewaretoken]').value
        // };

        // this.headers.append("Access-Control-Allow-Origin", "*")
        // this.headers.append("X-CSRFTOKEN", document.querySelector('[name=csrfmiddlewaretoken]').value)

        let thisrequest = '/mediaresources/'
        if (params) {
            thisrequest += params
        }

        this.client = fetch(thisrequest, {
            method: 'get',
            mode: 'same-origin',
            credentials: 'same-origin',
            headers: this.headers,
            redirect: 'follow'
        })
        return this.client
    }

    senderclient = (files) => {
        // let headers = {
        //     'Access-Control-Allow-Origin': '*',
        //     'X-CSRFTOKEN': document.querySelector('[name=csrfmiddlewaretoken]').value
        // };
        // let headers = new Headers();
        // headers.append('Access-Control-Allow-Origin', '*')

        const data = new FormData();

        for (const [i, file] of files.entries()) {
            // console.log('%d: %s', i, value);
            // data.append(`files-${i}`, file, file.name)
            data.append(`file`, file, file.name)
        }


        // data.append('audiofile', files[0], files[0].name)
        // for (const file of files) {
        //     data.append('files[]', file, file.name);
        // }
        // this.headers.append('content-type', files[0].type);
        // this.headers.append('content-length', files[0].size);

        this.client = fetch('/mediaresources/', {
            method: 'post',
            mode: 'same-origin',
            credentials: 'same-origin',
            headers: this.headers,
            redirect: 'follow',
            body: data
        })
        return this.client
    }

    getMediaResourcesList = (params) => {
        return this.init(params)
    }

    uploadFiles = (files) => {
        return this.senderclient(files)
    }
}
