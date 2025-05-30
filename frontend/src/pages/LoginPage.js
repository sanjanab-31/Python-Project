import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/LoginPage.css';
import backgroundImage from '../assets/istockphoto-1257951336-612x612.jpg';

const LoginPage = () => {
  useEffect(() => {
    // Prevent scrolling on mount
    document.body.style.overflow = 'hidden';
    // Re-enable scrolling on unmount
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');

  // Default credentials
  const defaultUsername = 'admin';
  const defaultPassword = 'admin123';

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (credentials.username === defaultUsername && credentials.password === defaultPassword) {
      // Set authentication status in localStorage
      localStorage.setItem('isAuthenticated', 'true');
      // Redirect to input page
      navigate('/input');
    } else {
      setError('Invalid username or password');
    }
  };

  return (
    <div className="login-container" style={{ backgroundImage: `url(${backgroundImage})` }}>
      <div className="login-form">
        <h2 className="login-title">Login</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={credentials.username}
              onChange={handleChange}
              placeholder="Enter username"
              required
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={credentials.password}
              onChange={handleChange}
              placeholder="Enter password"
              required
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="login-button">
            Login
          </button>
          <div className="default-credentials">
            <small>Default Credentials:</small>
            <small>Username: admin</small>
            <small>Password: admin123</small>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
