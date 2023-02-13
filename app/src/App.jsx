import './App.css';
import { Route, Routes, Link, Outlet } from 'react-router-dom'
import Home from './components/Home'
import Login from './components/accounts/Login'
import Unauthorized from './components/Unauthorized'
import Register from './components/accounts/Register'
import Missing from './components/Missing'

import Layout from './components/Layout'

import RequireAuth from './components/RequireAuth';

function App() {
  return (
    <>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/accounts/login/">Log in</Link>
          </li>
        </ul>
      </nav>
      <Routes>
        {/* <Route path="/accounts/login/" element={<Login />} /> */}
        <Route path="/" element={<Outlet />} >
          {/* public routes */}
          <Route path="/accounts" element={<Outlet />} >
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
          </Route>
          <Route path="unauthorized" element={<Unauthorized />} />

          {/* protected routes */}
          {/* <Route element={<RequireAuth />}>
          </Route> */}
            <Route path="" element={<Home />} />

          {/* missing */}
          <Route path="*" element={<Missing />} />

        </Route>
      </Routes>
    </>
  );
}

export default App;
