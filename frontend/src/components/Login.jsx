// src/components/Login.jsx
import React, { useState } from 'react'
import './Login.css'

export default function Login({ onSwitch }) {
  const [userId, setUserId]     = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = e => {
    e.preventDefault()
    console.log('Logging in with', { userId, password })
    // → your auth logic here
  }

  return (
    <div className="auth-card">
      <h2 className="auth-title">Log In</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        {/* User ID field */}
        <input
          type="text"
          placeholder="User ID"
          value={userId}
          onChange={e => setUserId(e.target.value)}
          required
        />

        {/* Password field */}
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />

        {/* Forgot-password link */}
        <div className="forgot-link">
          <a href="/forgot-password">Forgot Password?</a>
        </div>

        {/* Log In button */}
        <button type="submit" className="primary-btn">
          Log In
        </button>

        <hr className="divider" />

        {/* Sign-up prompt */}
        <div className="signup-prompt">
          Don’t have an account?{' '}
          <a href="/signup" className="signup-link">
            Sign Up
          </a>
        </div>
      </form>
    </div>
  )
}
