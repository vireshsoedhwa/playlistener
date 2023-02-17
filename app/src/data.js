

export default class Api {

    constructor() {
        // this.api_token = null;
        this.client = null;
        this.api_url = process.env.REACT_APP_API_ENDPOINT;
    }

    init = () => {
        // this.api_token = getCookie("ACCESS_TOKEN");

        // let headers = {
        //     'Access-Control-Allow-Origin': '*',
        //     'Content-Type': 'application/json',
        //     'X-CSRFTOKEN': document.querySelector('[name=csrfmiddlewaretoken]').value
        // };

        // if (this.api_token) {
        //   headers.Authorization = `Bearer ${this.api_token}`;
        // }

        this.client = fetch('/mediaresources/', {
            method: 'get',
            mode: 'same-origin',
            credentials: 'same-origin',
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
                'X-CSRFTOKEN': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            redirect: 'follow'
        }).then(response => {
            if (response.ok) {
                return response.json()
            }
        })
            .then(data => {
                console.log(data)
                return data
            })
            .catch(error => {
                console.error(error)
            })
    }

    getMediaResourcesList = (params) => {

        return this.init()
    }
}
    //   getUserList = (params) => {
    //     return this.init().get("/users", { params: params });
    //   };




//     fetch('/mediaresources/', {
//         method: 'get',
//         mode: 'same-origin',
//         credentials: 'same-origin',
//         headers: {
//             'Access-Control-Allow-Origin': '*',
//             'Content-Type': 'application/json',
//             'X-CSRFTOKEN': document.querySelector('[name=csrfmiddlewaretoken]').value
//         },
// redirect: 'follow'
//     })
//         .then(response => {
//     if (response.ok) {
//         console.log("")
//         return response.json()
//     }
// })
//     .then(data => {
//         // console.log(data)
//         return data
//     })
//     .catch(error => {
//         console.error(error)
//     })
// }
