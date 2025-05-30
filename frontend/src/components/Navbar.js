import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/Navbar.css';

const Navbar = () => {
  const navigate = useNavigate();
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <span>RAINWATER</span>
          <span style={{ display: 'block', fontSize: '1.5rem' }}>HARVESTER</span>
        </Link>
        <div className="nav-links">
          <Link to="/">Home</Link>
          {isAuthenticated ? (
            <>
              <Link to="/input">Input</Link>
              <Link to="/analysis">Analysis</Link>
              <Link to="/results">Results</Link>
              <Link to="/settings">Settings</Link>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </>
          ) : (
            <Link to="/login" className="login-link">Login</Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
