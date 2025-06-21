import React, { useState } from 'react';
import './CreateProfile.css';

export default function CreateProfile() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    userId: '',
    password: ''
  });
  const [message, setMessage] = useState('');

  const handleChange = e => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    const { firstName, lastName, email, userId, password } = formData;

    if (!firstName || !lastName || !email || !userId || !password) {
      setMessage('Please fill out all fields.');
      return;
    }

    try {
      // Combine first + last into single user_name field
      const user_name = `${firstName} ${lastName}`;

      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/user`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: 'eupn',
            uid: userId,
            pwd: password,
            email,
            user_name
          })
        }
      );

      const data = await res.json();
      console.log('[Signup] response status:', res.status);
      console.log('[Signup] response JSON:', data);

      if (data.status) {
        setMessage('✅ Profile created! You’re signed in.');
        // Store your JWT for later authenticated calls:
        localStorage.setItem('authToken', data.jwt);
        // Optionally redirect to dashboard:
        // navigate('/dashboard');
      } else {
        // The API returns detail.status for errors like "user exists"
        setMessage(`Error: ${data.detail?.status || 'Signup failed'}`);
      }
    } catch (err) {
      console.error(err);
      setMessage('Network error — please try again.');
    }
  };

  return (
    <div className="create-profile-container">
      <div className="profile-card">
        <h2>Create an account</h2>
        <form onSubmit={handleSubmit} className="profile-form">
          <input
            name="firstName"
            type="text"
            placeholder="First name"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
          <input
            name="lastName"
            type="text"
            placeholder="Last name"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
          <input
            name="email"
            type="email"
            placeholder="Email address"
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
            placeholder="New password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <button type="submit">Sign Up</button>
        </form>

        {message && <p className="profile-message">{message}</p>}
        <p className="profile-message">
          Already have an account? <a href="/login">Log in</a>
        </p>
      </div>
    </div>
  );
}