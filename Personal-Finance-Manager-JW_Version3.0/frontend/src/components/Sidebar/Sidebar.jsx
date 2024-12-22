import React from 'react';
import './Sidebar.css';

const Sidebar = ({ onPageChange }) => {
    return (
        <div className="sidebar">
            <button className="sidebar-button" onClick={() => onPageChange('reports')}>Reports</button>
            <button className="sidebar-button" onClick={() => onPageChange('expenses')}>Expenses</button>
            <button className="sidebar-button" onClick={() => onPageChange('income')}>Income</button>
            <button className="sidebar-button" onClick={() => onPageChange('budget')}>Budget</button>
        </div>
    );
};

export default Sidebar;
