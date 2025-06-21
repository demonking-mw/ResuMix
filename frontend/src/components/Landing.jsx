import React from 'react'
import './Landing.css'
import logo from '../assets/logo.png'

export default function Landing() {
  return (
    <div className="landing-container">
      {/* NAVIGATION */}
      <nav className="navbar">
        <img src={logo} alt="ResuMix Logo" className="logo" />
        <ul className="nav-links">
          <li><a href="#how-it-works">How it works</a></li>
          <li><a href="#help">Help</a></li>
        </ul>
        <div className="nav-actions">
          <a href="/login" className="login-link">Log in</a>
          <a href="/signup" className="signup-btn">Sign up ↗</a>
        </div>
      </nav>

      {/* HERO */}
      <header className="hero">
        <div className="hero-content">
          <h1>
            AI-Powered Resumes.<br/>
            Tailored to Every Job.
          </h1>
          <p>
            Upload your master resume once, then generate the perfect,
            job-specific resume in seconds.
          </p>
        </div>
      </header>

      {/* HOW IT WORKS */}
      <section id="how-it-works" className="placeholder">
        How It Works section…
      </section>

      {/* HELP */}
      <section id="help" className="placeholder">
        Help section…
      </section>
    </div>
  )
}
