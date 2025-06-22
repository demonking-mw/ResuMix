import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './CreateProfile.css';
import logo from '../assets/ResuMix.png';

export default function CreateProfile() {
  const [formData, setFormData] = useState({
    firstName: '', lastName:'', email:'', userId:'', password:''
  });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = e => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    const { firstName, lastName, email, userId, password } = formData;
    if (!firstName||!lastName||!email||!userId||!password) {
      setMessage('Please fill out all fields.');
      return;
    }
    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/user`,
        {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            type: 'eupn',
            uid: userId,
            pwd: password,
            email,
            user_name: `${firstName} ${lastName}`
          })
        }
      );
      const data = await res.json();
      if (data.status) {
        localStorage.setItem('authToken', data.jwt);
        navigate('/home');
      } else {
        setMessage(`Error: ${data.detail?.status || 'Signup failed'}`);
      }
    } catch {
      setMessage('Network error — please try again.');
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-header">
        <Link to="/" className="logo-link">
          <img src={logo} alt="ResuMix Logo" className="logo" />
          <span className="brand-name">ResuMix</span>
        </Link>
      </div>

      <div className="auth-card">
        <h2 className="auth-title">Create an Account</h2>
        <form className="auth-form" onSubmit={handleSubmit}>
          <input
            name="firstName"
            type="text"
            placeholder="First Name"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
          <input
            name="lastName"
            type="text"
            placeholder="Last Name"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
          <input
            name="email"
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            name="userId"
            type="text"
            placeholder="User ID"
            value={formData.userId}
            onChange={handleChange}
            required
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />

          {message && <p className="error-message">{message}</p>}

          <button type="submit" className="primary-btn">Sign Up</button>

          <hr className="divider" />

          <div className="signup-prompt">
            Already have an account?{' '}
            <Link to="/login" className="signup-link">Log In</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
