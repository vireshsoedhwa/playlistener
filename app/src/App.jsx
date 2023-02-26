import './App.css';
import { Route, Routes, Link, Outlet } from 'react-router-dom'
import Home from './components/Home'
import Login from './components/accounts/Login'
import Unauthorized from './components/Unauthorized'
import Register from './components/accounts/Register'
import Missing from './components/Missing'

import Layout from './components/Layout'

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Outlet />} >
          {/* public routes */}
          <Route path="/accounts" element={<Outlet />} >
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
          </Route>
          <Route path="unauthorized" element={<Unauthorized />} />

          <Route path="" element={<Home />} />

          {/* missing */}
          <Route path="*" element={<Missing />} />

        </Route>
      </Routes>
    </>
  );
}

export default App;
