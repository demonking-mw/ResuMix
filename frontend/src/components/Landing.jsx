import React from 'react';
import './Landing.css';
import logo from '../assets/ResuMix.png'; // adjust if needed

const Landing = () => {
  return (
    <div className="landing-container">
      <header className="navbar">
        <div className="logo-container">
          <img src={logo} alt="Logo" className="logo" />
          <span className="brand-name">ResuMix</span>
        </div>
        <div className="nav-actions">
          <a href="/login" className="landing-button">Log in</a>
          <a href="/signup" className="landing-button">Sign up ↗</a>
        </div>
      </header>

      <main className="hero">
        <div className="hero-content">
          <h1>
            AI-Powered Resumes. <br />
            Tailored to Every Job.
          </h1>
          <p>
            Upload your master resume once, then generate the perfect, job-specific resume in seconds.
          </p>
        </div>
      </main>
    </div>
  );
};

export default Landing;
