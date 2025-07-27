import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './CreateProfile.css';
import logo from '../assets/ResuMix.png';
import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import api from '../api/connection';
import { useAuth } from '../context/AuthContext';

export default function CreateProfile() {
  const [formData, setFormData] = useState({
    firstName: '', lastName:'', email:'', userId:'', password:''
  });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

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
      const response = await api.post('/user', {
        type: 'eupn',
        uid: userId,
        pwd: password,
        email,
        user_name: `${firstName} ${lastName}`
      });

      const data = response.data;

      if (data.status) {
        // Clear any previous error messages on successful signup
        setMessage('');
        
        // Extract user data from the backend response
        const userDetails = data.detail;
        const userData = {
          id: userId,
          email: email,
          name: `${firstName} ${lastName}`,
          // Add other fields as available from your database
        };
        
        // Use auth context login method with user data
        login(data.jwt, userData);
        navigate('/account');
      } else {
        const detail = data.detail?.status || data.message;
        if (detail === 'uid or email unique violation') {
          setMessage('User ID or email already exists');
        } else {
          setMessage(`Error: ${detail}`);
        }
      }
    } catch (err) {
      console.error('Signup error:', err);
      // Check if it's an axios error with response
      if (err.response && err.response.data) {
        const detail = err.response.data.detail?.status || err.response.data.message;
        if (detail === 'uid or email unique violation') {
          setMessage('User ID or email already exists');
        } else {
          setMessage(`Error: ${detail}`);
        }
      } else {
        setMessage('Network error — please try again later.');
      }
    }
  };

  const handleGoogleLoginSuccess = async (credentialResponse) => {
    if (credentialResponse.credential) {
      const decodedCredential = jwtDecode(credentialResponse.credential);
      const currentTime = Math.floor(Date.now() / 1000);
      const { iat, exp } = decodedCredential;
      
      // Check if the credential is timely
      if (currentTime < iat || currentTime > exp) {
        console.log("Credential is not valid: expired or issued in the future");
        setMessage("Google signup failed: Invalid credential timing");
      } else {
        console.log(decodedCredential);
        
        // Send the JWT to backend for signup/login using axios
        try {
          const response = await api.post("/user", {
            type: "go",
            jwt_token: credentialResponse.credential,
          });
          console.log("User authenticated:", response.data);
          
          if (response.data.status) {
            // Clear any previous error messages on successful signup/login
            setMessage('');
            
            // Use auth context login method with Google user data
            const userData = {
              id: decodedCredential.sub,
              email: decodedCredential.email,
              name: decodedCredential.name,
              picture: decodedCredential.picture,
            };
            login(response.data.jwt, userData);
            navigate('/account');
          } else {
            const detail = response.data.detail?.status || response.data.message;
            if (detail === 'auth type mismatch') {
              setMessage("An account with this email already exists using a different login method");
            } else {
              setMessage(`Google signup failed: ${detail}`);
            }
          }
        } catch (err) {
          console.error("Error with Google signup:", err);
          // Check if it's an axios error with response
          if (err.response && err.response.data) {
            const detail = err.response.data.detail?.status || err.response.data.message;
            if (detail === 'auth type mismatch') {
              setMessage("An account with this email already exists using a different login method");
            } else {
              setMessage(`Google signup failed: ${detail}`);
            }
          } else {
            setMessage("Google signup failed: Network error");
          }
        }
      }
    } else {
      console.log("Credential is undefined");
      setMessage("Google signup failed: No credential received");
    }
  };

  return (
    <GoogleOAuthProvider clientId="934728058727-jvm3keubjaluikeg06hl4voifiq8fcv0.apps.googleusercontent.com">
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

            {message && (
              <div className="error-container">
                <span className="error-message">{message}</span>
                {message === 'User ID or email already exists' && (
                  <Link to="/login" className="signup-redirect-btn">
                    Log In
                  </Link>
                )}
              </div>
            )}

            <button type="submit" className="primary-btn">Sign Up</button>

            <hr className="divider" />

            {/* Google OAuth Signup Button */}
            <div className="google-login-container" style={{ marginBottom: '0px', textAlign: 'center' }}>
              <GoogleLogin
                onSuccess={handleGoogleLoginSuccess}
                onError={() => {
                  console.log("Google Signup Failed");
                  setMessage("Google signup failed");
                }}
              />
            </div>

            <hr className="divider" />

            <div className="signup-prompt">
              Already have an account?{' '}
              <Link to="/login" className="signup-link">Log In</Link>
            </div>
          </form>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}
