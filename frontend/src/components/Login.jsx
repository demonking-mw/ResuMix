// src/components/Login.jsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Login.css';

export default function Login() {
  const [userId, setUserId]     = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    setErrorMessage('');

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
          body: JSON.stringify({ type:'up', uid:userId, pwd:password })
        }
      );
      const data = await res.json();

      if (res.ok && data.status) {
        localStorage.setItem('authToken', data.jwt);
        navigate('/home');
      } else {
        const detail = data.detail?.status || data.message;
        if (detail === 'user not found') {
          setErrorMessage('User not found. Please check your User ID.');
        } else if (detail === 'password incorrect') {
          setErrorMessage('Incorrect password. Please try again.');
        } else {
          setErrorMessage(`Error: ${detail}`);
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
          <Link to="/forgot-password">Forgot Password?</Link>
        </div>

        <button type="submit" className="primary-btn">Log In</button>

        <hr className="divider" />

        <div className="signup-prompt">
          Don’t have an account?{' '}
          <Link to="/signup" className="signup-link">Sign Up</Link>
        </div>
      </form>
    </div>
  );
}