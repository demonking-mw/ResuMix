// src/components/Login.jsx
import React, { useState } from 'react';
import './Login.css';

export default function Login() {
  const [userId, setUserId]         = useState('');
  const [password, setPassword]     = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    setErrorMessage('');

    // simple client‐side check
    if (!userId || !password) {
      setErrorMessage('Please fill out both User ID and Password.');
      return;
    }

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/user`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: 'up',     // “up” = username+password login
            uid: userId,
            pwd: password
          })
        }
      );

      const data = await res.json();
      console.log('[Login] response:', res.status, data);

      // status=true means success
      if (res.ok && data.status) {
        localStorage.setItem('authToken', data.jwt);
        // redirect or reload as needed; for now:
        alert('✅ Logged in successfully!');
      } else {
        // Map backend's detail.status to friendly text
        const detail = data.detail?.status || data.message;
        if (detail === 'user not found') {
          setErrorMessage('User not found. Please check your User ID.');
        } else if (detail === 'password incorrect') {
          setErrorMessage('Incorrect password. Please try again.');
        } else {
          setErrorMessage(`Error: ${detail || 'Login failed'}`);
        }
      }
    } catch (err) {
      console.error('Login error:', err);
      setErrorMessage('Network error — please try again later.');
    }
  };

  return (
    <div className="auth-card">
      <h2 className="auth-title">Log In</h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="User ID"
          value={userId}
          onChange={e => setUserId(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />

        {errorMessage && <p className="error-message">{errorMessage}</p>}

        <div className="forgot-link">
          <a href="/forgot-password">Forgot Password?</a>
        </div>

        <button type="submit" className="primary-btn">Log In</button>

        <hr className="divider" />

        <div className="signup-prompt">
          Don’t have an account?{' '}
          <a href="/signup" className="signup-link">Sign Up</a>
        </div>
      </form>
    </div>
  );
}