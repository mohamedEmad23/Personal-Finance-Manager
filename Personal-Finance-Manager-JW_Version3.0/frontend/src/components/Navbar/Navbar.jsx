import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { FaUserCircle } from 'react-icons/fa';
import api from '../../api';
import './Navbar.css';

const Navbar = () => {
  const [isDropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const toggleDropdown = () => {
    setDropdownOpen(!isDropdownOpen);
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken'); // Assuming the token is stored in localStorage
    navigate('/login');
  };

  const location = useLocation();
  const { userId } = location.state || {};
  const [userName, setUserName] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (userId) {
      api.get(`users/users/${userId}`)
        .then((response) => {
          if (response.data.name) {
            setUserName(response.data.name);
          } else {
            console.error('User not found');
          }
          setLoading(false);
        })
        .catch((error) => {
          console.error('Error fetching user data:', error);
          setLoading(false);
        });
    }
  }, [userId]);

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>FinWise</h1>
      </div>
      <div className="navbar-center">
        {loading ? (
          <h2>Loading user data...</h2>
        ) : (
          <h2>Welcome to your Dashboard, {userName || "User not found"}!</h2>
        )}
      </div>
      <div className="profile">
        <FaUserCircle size={30} onClick={toggleDropdown} />
        {isDropdownOpen && (
          <div className="dropdown">
            <button onClick={handleLogout}>Logout</button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;