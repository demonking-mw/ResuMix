import React, { useState } from 'react';
import './CreateProfile.css';

const CreateProfile = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    userId: '',
    password: ''
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const { firstName, lastName, email, userId, password } = formData;

    if (!firstName || !lastName || !email || !userId || !password) {
      setMessage('Please fill out all fields.');
      return;
    }

    // Future: send to backend API
    console.log('Profile Created:', formData);
    setMessage('Profile successfully created!');
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

        {/* Optional: redirect link */}
        <p className="profile-message">
          Already have an account? <a href="/login">Log in</a>
        </p>
      </div>
    </div>
  );
};

export default CreateProfile;