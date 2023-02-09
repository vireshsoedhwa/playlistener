import React, { Fragment, useEffect, useState, useRef } from 'react';

export default function App() {
    const [values, setValues] = React.useState({
        username: '',
        password: '',
        showPassword: false,
        authFailed: false
    });

    const [usernameError, setusernameError] = React.useState(false)
    const [passwordError, setpasswordError] = React.useState(false)
    const [disableSubmit, setdisableSubmit] = React.useState(true)

    useEffect(() => {
        if (values.username == '' || values.password == '') {
            setdisableSubmit(true)
        } else {
            setdisableSubmit(false)
        }
    }, [values]);

    const handleChange = (prop) => (event) => {
        setValues({ ...values, [prop]: event.target.value });
    };

    const handleClickShowPassword = () => {
        setValues({
            ...values,
            showPassword: !values.showPassword,
        });
    };

    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };

    const handleSubmit = (event) => {
        if (values.username == '') {
            setusernameError(true)
        }
        if (values.password == '') {
            setpasswordError(true)
        }

        event.preventDefault();
        const formData = new FormData();
        const request = new Request('/accounts/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'username': values.username,
                'password': values.password
            })
        });

        fetch(request)
            .then((response) => {
                console.log(response)
                if (response.redirected) {
                    window.location.href = response.url;
                }
                else {
                    setValues({
                        ...values,
                        authFailed: true,
                        username: '',
                        password: '',
                    });
                }
            })
            .catch((error) => console.error(error));
    }


    return (
        <div>
            <h1 className="text-3xl font-bold underline">
                Hello world!
            </h1>
            inside LOGIN PAGE component

        </div >
    )
}