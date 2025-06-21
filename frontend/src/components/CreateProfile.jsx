// src/components/CreateProfile.jsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './CreateProfile.css';

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
    <div className="create-profile-container">
      <div className="profile-card">
        <h2>Create an account</h2>
        <form onSubmit={handleSubmit} className="profile-form">
          <input
            name="firstName" type="text" placeholder="First name"
            value={formData.firstName} onChange={handleChange} required
          />
          <input
            name="lastName" type="text" placeholder="Last name"
            value={formData.lastName} onChange={handleChange} required
          />
          <input
            name="email" type="email" placeholder="Email address"
            value={formData.email} onChange={handleChange} required
          />
          <input
            name="userId" type="text" placeholder="User ID"
            value={formData.userId} onChange={handleChange} required
          />
          <input
            name="password" type="password" placeholder="New password"
            value={formData.password} onChange={handleChange} required
          />
          <button type="submit">Sign Up</button>
        </form>

        {message && <p className="profile-message">{message}</p>}

        <p className="profile-message">
          Already have an account?{' '}
          <Link to="/login">Log In</Link>
        </p>
      </div>
    </div>
  );
}