// src/components/Login.jsx
import React, { useState } from 'react';
import './Login.css';

export default function Login({ onSwitch }) {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: 'up', // "up" means "user password" login
          uid: userId,
          pwd: password,
        }),
      });

      const data = await res.json();
      console.log('[Login] response:', data);

      if (res.ok && data.status) {
        // Successful login
        localStorage.setItem('authToken', data.jwt); // Save token
        setErrorMessage('');
        alert('✅ Logged in!');
        // Optionally redirect to dashboard
        // navigate('/dashboard');
      } else {
        setErrorMessage(data.detail?.status || 'Invalid credentials');
      }
    } catch (err) {
      console.error('Login error:', err);
      setErrorMessage('⚠️ Not able to log in. Please try again later.');
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
