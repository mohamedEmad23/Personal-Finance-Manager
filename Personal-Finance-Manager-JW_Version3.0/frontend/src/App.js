import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Login from './components/Auth/Login';
import Register from './components/Auth/register';
import Home from './components/Home/Home';
import Dashboard from './components/Dashboard/Dashboard';
import { UserProvider } from './contexts/UserContext';
import { IncomeProvider } from './contexts/IncomeContext';

const App = () => {
  return (
    <UserProvider>
      <IncomeProvider>
        <Router>
          <ToastContainer />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </Router>
      </IncomeProvider>
    </UserProvider>
  );
};

export default App;