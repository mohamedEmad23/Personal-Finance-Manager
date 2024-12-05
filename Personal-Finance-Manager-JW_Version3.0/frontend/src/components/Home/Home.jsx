import React from 'react';
import './Home.css';
import { useNavigate } from 'react-router-dom';

const Home = () => {
    const navigate = useNavigate();
    return (
        <div className="home-container">
            <div className="title-container">
                <h1 className="title">Welcome to FinWise</h1>
            </div>
            <div className="description">
                <h1>Your Finances, Simplified</h1>
                <p>
                    Manage your finances with ease. Track your expenses, set budgets, and achieve your financial goals.
                </p>
                <div className="icons-container">
                    <img src="/images/in-out.png" alt="Transactions Icon" className="icon" />
                    <img src="/images/budget.png" alt="Budget Icon" className="icon" />
                    <img src="/images/report.png" alt="Report Icon" className="icon" />
                </div>
            </div>
            <div className="actions">
                <button className="register-btn" onClick={() => navigate('/register')}>Register</button>
                <button className="login-btn" onClick={() => navigate('/login')}>Login</button>
            </div>
        </div>
    );
};

export default Home;
