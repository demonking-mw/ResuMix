// src/components/Login.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './Login.css';
import logo from '../assets/ResuMix.png';
import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";
import api from '../api/connection';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  // Debug component lifecycle
  useEffect(() => {
    console.log('Login component mounted/re-rendered');
    console.log('Current errorMessage:', errorMessage);
    console.log('Current userId:', userId);
    console.log('Current password length:', password.length);
  });

  // Get the intended destination (where user was trying to go before login)
  const from = location.state?.from?.pathname || '/account';

  const handleSubmit = async (e) => {
    console.log('handleSubmit called, event:', e);
    e.preventDefault();
    e.stopPropagation();
    console.log('Form submission prevented');
    
    if (!userId || !password) {
      console.log('Missing fields, setting error message');
      setErrorMessage('Please fill out both User ID and Password.');
      return;
    }

    console.log('Starting API call...');

    try {
      const response = await api.post('/user', {
        type: 'up', 
        uid: userId, 
        pwd: password
      });

      const data = response.data;

      if (data.status) {
        // Clear any previous error messages on successful login
        setErrorMessage('');
        
        // Extract user data from the backend response
        const userDetails = data.detail;
        const userData = {
          id: userDetails.uid,
          email: userDetails.email,
          name: userDetails.user_name || userDetails.uid, // Use user_name if available, fallback to uid
          // Add other fields as available from your database
        };
        
        // Use auth context login method with user data
        login(data.jwt, userData);
        navigate(from, { replace: true });
      } else {
        console.log('Login failed, response data:', data);
        const detail = data.detail?.status || data.message;
        console.log('Error detail:', detail);
        if (detail === 'user not found') {
          setErrorMessage('UID not found');
        } else if (detail === 'password incorrect') {
          // Only set the message if it's different to avoid re-render flash
          if (errorMessage !== 'Password incorrect') {
            console.log('Setting password incorrect error message');
            try {
              setErrorMessage('Password incorrect');
              console.log('Password incorrect message set successfully');
            } catch (err) {
              console.error('Error setting password incorrect message:', err);
            }
          } else {
            console.log('Skipping password incorrect message - already set');
          }
          // TODO: Clear the password field but keep the UID - temporarily disabled
          // setPassword('');
        } else {
          setErrorMessage(`Error: ${detail}`);
        }
      }
    } catch (err) {
      console.error('Login error caught:', err);
      console.log('Error response:', err.response);
      // Check if it's an axios error with response
      if (err.response && err.response.data) {
        const detail = err.response.data.detail?.status || err.response.data.message;
        console.log('Catch block error detail:', detail);
        if (detail === 'user not found') {
          setErrorMessage('UID not found');
        } else if (detail === 'password incorrect') {
          // Only set the message if it's different to avoid re-render flash
          if (errorMessage !== 'Password incorrect') {
            console.log('Catch: Setting password incorrect error message');
            setErrorMessage('Password incorrect');
          } else {
            console.log('Catch: Skipping password incorrect message - already set');
          }
        } else {
          setErrorMessage(`Error: ${detail}`);
        }
      } else {
        setErrorMessage('Network error — please try again later.');
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
        setErrorMessage("Google login failed: Invalid credential timing");
      } else {
        console.log(decodedCredential);
        
        // Send the JWT to backend for login using axios
        try {
          const response = await api.post("/user", {
            type: "go",
            jwt_token: credentialResponse.credential,
          });
          console.log("User authenticated:", response.data);
          
          if (response.data.status) {
            // Use auth context login method with Google user data
            const userData = {
              id: decodedCredential.sub,
              email: decodedCredential.email,
              name: decodedCredential.name,
              picture: decodedCredential.picture,
            };
            login(response.data.jwt, userData);
            navigate(from, { replace: true });
          } else {
            setErrorMessage("Google login failed: " + (response.data.detail?.status || response.data.message));
          }
        } catch (err) {
          console.error("Error with Google login:", err);
          setErrorMessage("Google login failed: Network error");
        }
      }
    } else {
      console.log("Credential is undefined");
      setErrorMessage("Google login failed: No credential received");
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
            {errorMessage && (
              <div className="error-container">
                <span className="error-message">{errorMessage}</span>
                {errorMessage === 'UID not found' && (
                  <Link to="/signup" className="signup-redirect-btn">
                    Sign Up
                  </Link>
                )}
              </div>
            )}

            <div className="forgot-link">
              <Link to="/forgot-password">Forgot Password?</Link>
            </div>

            <button 
              type="submit" 
              className="primary-btn"
            >
              Log In
            </button>
            
            <hr className="divider" />
            
            {/* Google OAuth Login Button */}
            <div className="google-login-container" style={{ marginBottom: '20px', textAlign: 'center' }}>
              <GoogleLogin
                onSuccess={handleGoogleLoginSuccess}
                onError={() => {
                  console.log("Google Login Failed");
                  setErrorMessage("Google login failed");
                }}
              />
            </div>
            
            <hr className="divider" />
            <div className="signup-prompt">
              Don't have an account?{' '}
              <Link to="/signup" className="signup-link">Sign Up</Link>
            </div>
          </form>
        </div>
      </div>
    </GoogleOAuthProvider>
  );
}
