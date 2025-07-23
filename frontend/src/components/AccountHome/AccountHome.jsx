// src/components/AccountHome/AccountHome.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './AccountHome.css';
import logo from '../../assets/ResuMix.png';

const AccountHome = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  // Debug: Let's see what's in the user object
  console.log('User object in AccountHome:', user);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="account-container">
      {/* Header with Logo and User Actions */}
      <header className="account-header">
        <Link to="/account" className="logo-link">
          <img src={logo} alt="ResuMix Logo" className="logo" />
          <span className="brand-name">ResuMix</span>
        </Link>
        <div className="user-actions">
          <span className="welcome-text">Welcome, {user?.name || user?.user_name || user?.id || 'User'}!</span>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      {/* Status Bar */}
      <div className="status-bar">
        <div className="status-content">
          <span className="status-text">STATUS BAR</span>
        </div>
      </div>

      {/* Main Content */}
      <main className="account-main">
        <div className="workflow-container">
          {/* Step 1: Master Resume */}
          <div className="workflow-step">
            <div className="status-indicator">
              <span className="status-label">&lt;STATUS_INDICATOR&gt;</span>
            </div>
            <div className="step-card">
              <div className="step-content">
                <Link to="/master-resume" className="step-link">
                  Set your master resume
                </Link>
                <p className="step-description">
                  Upload and configure your comprehensive resume template
                </p>
              </div>
            </div>
          </div>

          {/* Step 2: Parameters */}
          <div className="workflow-step">
            <div className="status-indicator">
              <span className="status-label">&lt;STATUS_INDICATOR&gt;</span>
            </div>
            <div className="step-card">
              <div className="step-content">
                <span className="step-title">Tweak your resume's parameter</span>
                <p className="step-description">
                  Customize settings and preferences for resume optimization
                </p>
                <Link to="/parameters" className="step-button">Configure</Link>
              </div>
            </div>
          </div>

          {/* Step 3: Generate */}
          <div className="workflow-step">
            <div className="status-indicator">
              <span className="status-label">&lt;STATUS_INDICATOR&gt;</span>
            </div>
            <div className="step-card">
              <div className="step-content">
                <span className="step-title">Generate</span>
                <p className="step-description">
                  Create optimized resumes tailored to specific job opportunities
                </p>
                <Link to="/generate" className="step-button generate-btn">Generate</Link>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AccountHome;
