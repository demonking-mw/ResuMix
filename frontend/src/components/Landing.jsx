import React from 'react';
import './Landing.css';
import logo from '../assets/ResuMix.png'; // adjust path if needed

const Landing = () => {
  return (
    <div className="landing-container">
      <header className="navbar">
        <div className="logo-container">
          <img src={logo} alt="Logo" className="logo" />
          <span className="brand-name">ResuMix</span>
        </div>
        <nav className="nav-links">
          <a href="#how">How it works</a>
          <a href="#help">Help</a>
        </nav>
        <div className="nav-actions">
          <a href="/login" className="login-link">Log in</a>
          <a href="/signup" className="signup-btn">Sign up ↗</a>
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

      <section id="how" className="placeholder">How It Works section…</section>
      <section id="help" className="placeholder">Help section…</section>
    </div>
  );
};

export default Landing;
