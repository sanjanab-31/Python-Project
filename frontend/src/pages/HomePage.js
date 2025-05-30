import React from 'react';
import { Link } from 'react-router-dom';
import backgroundImage from '../assets/istockphoto-1257951336-612x612.jpg';
import '../styles/HomePage.css';
// Add Material Icons CSS
import '@fontsource/material-icons';

const HomePage = () => {
  return (
    <div className="container">
      <section className="hero-section" style={{ backgroundImage: `url(${backgroundImage})` }}>
        <div className="hero-overlay"></div>
        <div className="hero-content">
          <h1>IT'S TIME TO HARVEST NATURE</h1>
          <h2>SAVE RAIN, SAVE TOMORROW</h2>
          <p>
            Discover innovative rainwater conservation methods. Learn how small changes can make a big impact on your future.
          </p>
          <div className="hero-cta">
            <Link to="/input" className="btn btn-outline">
              Get Started
            </Link>
            <Link to="/analysis" className="btn btn-outline">
              View Analysis
            </Link>
          </div>
        </div>
      </section>

      <section className="features-section">
        <h2 className="section-title">Key Features</h2>
        <div className="features-carousel">
          <div className="feature-card">
            <span className="material-icons feature-icon">calculate</span>
            <h3>Real-Time Calculations</h3>
            <p>Get precise inflow calculations and smart recommendations based on your system parameters.</p>
          </div>
          <div className="feature-card">
            <span className="material-icons feature-icon">cloud</span>
            <h3>Weather Integration</h3>
            <p>Access real-time rainfall predictions using advanced weather APIs.</p>
          </div>
          <div className="feature-card">
            <span className="material-icons feature-icon">warning</span>
            <h3>Leak Detection</h3>
            <p>Smart alerts for abnormal water losses and maintenance recommendations.</p>
          </div>
          <div className="feature-card">
            <span className="material-icons feature-icon">savings</span>
            <h3>ROI Calculation</h3>
            <p>Track your savings and calculate system return on investment.</p>
          </div>
          <div className="feature-card">
            <span className="material-icons feature-icon">smart_toy</span>
            <h3>AI-Based Optimization</h3>
            <p>Get intelligent water usage recommendations for different purposes.</p>
          </div>
          <div className="feature-card">
            <span className="material-icons feature-icon">bar_chart</span>
            <h3>Visual Reports</h3>
            <p>Comprehensive analytics with interactive charts and graphs.</p>
          </div>
        </div>
      </section>

      <section className="how-it-works">
        <div className="steps-container">
          <h2>How It Works</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', marginTop: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <span className="step-number">1</span>
              <div>
                <h3>Input Your Data</h3>
                <p>Enter your system parameters in the <Link to="/input">Input page</Link>.</p>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <span className="step-number">2</span>
              <div>
                <h3>Weather Analysis</h3>
                <p>Our system fetches real-time weather data for your location.</p>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <span className="step-number">3</span>
              <div>
                <h3>Smart Calculations</h3>
                <p>Advanced algorithms optimize water usage and detect potential issues.</p>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <span className="step-number">4</span>
              <div>
                <h3>View Results</h3>
                <p>Get detailed insights and recommendations in the <Link to="/results">Results page</Link>.</p>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <span className="step-number">5</span>
              <div>
                <h3>Track Progress</h3>
                <p>Monitor performance trends in the <Link to="/analysis">Analysis page</Link>.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
