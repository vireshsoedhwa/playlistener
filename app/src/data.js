export default class Api {

    constructor() {
        // this.api_token = null;
        this.client = null;
        this.api_url = process.env.REACT_APP_API_ENDPOINT;
    }

    init = (params) => {
        // this.api_token = getCookie("ACCESS_TOKEN");

        // let headers = {
        //     'Access-Control-Allow-Origin': '*',
        //     'Content-Type': 'application/json',
        //     'X-CSRFTOKEN': document.querySelector('[name=csrfmiddlewaretoken]').value
        // };

        // if (this.api_token) {
        //   headers.Authorization = `Bearer ${this.api_token}`;
        // }
        let thisrequest = '/mediaresources/' 
        if (params) {
            thisrequest += params
        }

        this.client = fetch(thisrequest, {
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
        return this.client
    }

    getMediaResourcesList = (params) => {
        return this.init(params)
    }
}
