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
  const [totalIncome, setTotalIncome] = useState(0);
  const [loading, setLoading] = useState(true);

  // Track reload to refetch data
  const [reload, setReload] = useState(false);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        if (userId) {
          // Fetch user data
          const userResponse = await api.get(`users/users/${userId}`);
          if (userResponse.data.name) {
            setUserName(userResponse.data.name);
          } else {
            console.error('User not found');
          }
  
          // Fetch total income
          const incomeResponse = await api.get(`income/incomes/total/`, {
            params: { user_id: userId },
          });
          console.log('Income API response:', incomeResponse.data); // Log to inspect
          if (incomeResponse.data.total_income !== undefined) {
            setTotalIncome(incomeResponse.data.total_income); // Use `total_income`
          } else {
            console.error('Total income not found in response:', incomeResponse.data);
          }
        }
      } catch (error) {
        console.error('Error fetching user or income data:', error);
      } finally {
        setLoading(false);
      }
    };
  
    fetchUserData();
  }, [userId, reload]);
  

  const refreshIncome = () => {
    setReload(!reload); // Trigger refetch by toggling reload state
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>FinWise</h1>
      </div>
      <div className="navbar-center">
        {loading ? (
          <h2>Loading user data...</h2>
        ) : (
          <h2>
            Welcome to your Dashboard, {userName || 'User not found'}! 
            <br />
            Total Income: ${totalIncome.toFixed(2)}
          </h2>
        )}
      </div>
      <div className="profile">
        <FaUserCircle size={30} onClick={toggleDropdown} />
        {isDropdownOpen && (
          <div className="dropdown">
            <button onClick={refreshIncome}>Refresh Income</button>
            <button onClick={handleLogout}>Logout</button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
