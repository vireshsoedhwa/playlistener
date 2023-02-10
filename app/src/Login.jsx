import React, { Fragment, useEffect, useState, useRef } from 'react';

export default function App() {
    const [Values, setValues] = React.useState({
        username: '',
        password: '',
        showPassword: false,
        authFailed: false
    });

    const [usernameError, setusernameError] = React.useState(false)
    const [passwordError, setpasswordError] = React.useState(false)
    const [disableSubmit, setdisableSubmit] = React.useState(true)

    useEffect(() => {
        if (Values.username == '' || Values.password == '') {
            setdisableSubmit(true)
        } else {
            setdisableSubmit(false)
        }
    }, [Values]);

    // const handleChange = (prop) => (event) => {
    //     console.log("ayy")
    //     setValues({ ...values, [prop]: event.target.value });
    // };

    const handleChange = (prop) => (event) => {
        setValues({ ...Values, [prop]: event.target.value });
    };

    // const handleSubmit = (event) => {
    //     console.log("submit worked")
    // }

    const handleSubmit = (event) => {
        if (Values.username == '') {
            setusernameError(true)
        }
        if (Values.password == '') {
            setpasswordError(true)
        }

        console.log(event.target)

        event.preventDefault();
        // const formData = new FormData();
        // const request = new Request('/accounts/login/', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/x-www-form-urlencoded',
        //     },
        //     body: new URLSearchParams({
        //         'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        //         'username': Values.username,
        //         'password': Values.password
        //     })
        // });

        // fetch(request)
        //     .then((response) => {
        //         console.log(response)
        //         if (response.redirected) {
        //             window.location.href = response.url;
        //         }
        //         else {
        //             setValues({
        //                 ...Values,
        //                 authFailed: true,
        //                 username: '',
        //                 password: '',
        //             });
        //         }
        //     })
        //     .catch((error) => console.error(error));
    }


    return (
        <div class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <div class="w-full max-w-md space-y-8">
                <form class="mt-8 space-y-6" action="/accounts/login/" method="POST"
                    onSubmit={handleSubmit}>
                    <input type="hidden" name="remember" value="true" />
                    <div class="-space-y-px rounded-md shadow-sm">
                        <div>
                            <label for="email-address" class="sr-only">
                                Username</label>
                            <input id="email-address" name="email" type="text"
                                autocomplete="email" required
                                class="relative block w-full appearance-none rounded-none 
                            rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 
                            placeholder-gray-500 focus:z-10 focus:border-indigo-500 
                            focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                placeholder="Username"
                                onChange={handleChange("username")}
                            />
                        </div>
                        <div>
                            <label for="password" class="sr-only">
                                Password</label>
                            <input id="password" name="password" type="password"
                                autocomplete="current-password" required
                                class="relative block w-full appearance-none rounded-none 
                            rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 
                            placeholder-gray-500 focus:z-10 focus:border-indigo-500 
                            focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                placeholder="Password"
                                onChange={handleChange('password')}
                            />
                        </div>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center">
                            <input id="remember-me" name="remember-me" type="checkbox"
                                class="h-4 w-4 rounded border-gray-300 text-indigo-600 
                            focus:ring-indigo-500" />
                            <label for="remember-me"
                                class="ml-2 block text-sm text-gray-900">
                                Remember me</label>
                        </div>

                        {/* <div class="text-sm">
                            <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500">Forgot your password?</a>
                        </div> */}
                    </div>

                    <div>
                        <button
                            type="submit"
                            class="group relative flex w-full justify-center rounded-md border 
                            border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium 
                            text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 
                            focus:ring-indigo-500 focus:ring-offset-2"
                            value="Submit"
                            >
                            {/* <span class="absolute inset-y-0 left-0 flex items-center pl-3">
                                <svg class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                    <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd" />
                                </svg>
                            </span> */}
                            Sign in
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}