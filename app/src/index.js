import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import Login from './Login';
import reportWebVitals from './reportWebVitals';

// const index = ReactDOM.createRoot(document.getElementById('index'));

// index.render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>
// );

const login = ReactDOM.createRoot(document.getElementById('login'));

login.render(
  <React.StrictMode>
    <Login />
  </React.StrictMode>
);

// ReactDOM.render(
//   Login,
//   document.getElementById('login')
// );

// ReactDOM.render(
//   <h1>home</h1>,
//   document.getElementById('home')
// );

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
