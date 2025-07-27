// src/components/AccountHome/AccountHome.jsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './AccountHome.css';
import logo from '../../assets/ResuMix.png';

const AccountHome = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [showHelp, setShowHelp] = useState(null);

  // Debug: Let's see what's in the user object
  console.log('User object in AccountHome:', user);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleCardClick = (destination) => {
    // TODO: Implement navigation logic
    console.log(`Navigating to: ${destination}`);
    // navigate(destination);
  };

  const handleHelpClick = (e, stepNumber) => {
    e.stopPropagation(); // Prevent card click
    setShowHelp(showHelp === stepNumber ? null : stepNumber);
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
            <div className="step-card clickable-card" onClick={() => handleCardClick('/master-resume')}>
              <div className="step-content">
                <span className="step-title">Set your master resume</span>
                <p className="step-description">
                  Upload and configure your comprehensive resume template
                </p>
                <button 
                  className="step-button help-button" 
                  onClick={(e) => handleHelpClick(e, 1)}
                >
                  Help
                </button>
              </div>
            </div>
          </div>

          {/* Step 2: Parameters */}
          <div className="workflow-step">
            <div className="status-indicator">
              <span className="status-label">&lt;STATUS_INDICATOR&gt;</span>
            </div>
            <div className="step-card clickable-card" onClick={() => handleCardClick('/parameters')}>
              <div className="step-content">
                <span className="step-title">Tweak your resume's parameter</span>
                <p className="step-description">
                  Customize settings and preferences for resume optimization
                </p>
                <button 
                  className="step-button help-button" 
                  onClick={(e) => handleHelpClick(e, 2)}
                >
                  Help
                </button>
              </div>
            </div>
          </div>

          {/* Step 3: Generate */}
          <div className="workflow-step">
            <div className="status-indicator">
              <span className="status-label">&lt;STATUS_INDICATOR&gt;</span>
            </div>
            <div className="step-card clickable-card" onClick={() => handleCardClick('/generate')}>
              <div className="step-content">
                <span className="step-title">Generate</span>
                <p className="step-description">
                  Create optimized resumes tailored to specific job opportunities
                </p>
                <button 
                  className="step-button help-button" 
                  onClick={(e) => handleHelpClick(e, 3)}
                >
                  Help
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Help Information */}
        {showHelp && (
          <div className="help-section">
            <div className="help-content">
              <button 
                className="help-close-button" 
                onClick={() => setShowHelp(null)}
                aria-label="Close help"
              >
                ×
              </button>
              {showHelp === 1 && (
                <div className="help-info">
                  <h3>Master Resume Help</h3>
                  <p>Upload your complete resume template that contains all your experience, skills, and achievements. This will serve as the foundation for generating tailored resumes.</p>
                  <ul>
                    <li>Upload PDF or Word document</li>
                    <li>Include all relevant experience</li>
                    <li>Add comprehensive skills list</li>
                  </ul>
                </div>
              )}
              {showHelp === 2 && (
                <div className="help-info">
                  <h3>Parameters Help</h3>
                  <p>Configure settings that control how your resume is optimized for different job opportunities.</p>
                  <ul>
                    <li>Set keyword matching preferences</li>
                    <li>Choose resume sections to prioritize</li>
                    <li>Adjust optimization algorithms</li>
                  </ul>
                </div>
              )}
              {showHelp === 3 && (
                <div className="help-info">
                  <h3>Generate Help</h3>
                  <p>Create customized resumes tailored to specific job postings using your master resume and configured parameters.</p>
                  <ul>
                    <li>Paste job description</li>
                    <li>Select optimization level</li>
                    <li>Download tailored resume</li>
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default AccountHome;
