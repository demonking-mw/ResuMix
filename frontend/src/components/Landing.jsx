// src/components/Landing.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './Landing.css';
import logo from '../assets/ResuMix.png';

const Landing = () => (
  <div className="landing-container">
    <header className="navbar">
      <Link to="/" className="logo-link">
        <img src={logo} alt="ResuMix Logo" className="logo" />
        <span className="brand-name">ResuMix</span>
      </Link>
      <div className="nav-actions">
        <Link to="/login" className="landing-button">Log in</Link>
        <Link to="/signup" className="landing-button">Sign up ↗</Link>
      </div>
    </header>
    <main className="hero">
      <div className="hero-bubble">
        <h1>Optimize Your Resume.<br/>Maximize Your Impact.</h1>
        <p>
          Upload your resume once, then generate the perfect,
          job-specific resume in seconds.
        </p>
      </div>
    </main>
  </div>
);

export default Landing;
