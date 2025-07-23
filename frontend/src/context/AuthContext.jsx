// src/context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext({});

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  // Check if user is logged in on app start
  useEffect(() => {
    const checkAuthState = () => {
      try {
        const storedToken = localStorage.getItem('authToken');
        
        if (storedToken) {
          // Decode and validate the token
          const decodedToken = jwtDecode(storedToken);
          const currentTime = Math.floor(Date.now() / 1000);
          
          // Check if token is still valid
          if (decodedToken.exp && currentTime < decodedToken.exp) {
            setToken(storedToken);
            setUser({
              id: decodedToken.sub || decodedToken.user_id,
              email: decodedToken.email,
              name: decodedToken.name || decodedToken.given_name,
              picture: decodedToken.picture,
              // Add other user data from your JWT as needed
            });
          } else {
            // Token expired, clear it
            localStorage.removeItem('authToken');
          }
        }
      } catch (error) {
        console.error('Error checking auth state:', error);
        localStorage.removeItem('authToken');
      } finally {
        setLoading(false);
      }
    };

    checkAuthState();
  }, []);

  const login = (token, userData = null) => {
    try {
      setToken(token);
      localStorage.setItem('authToken', token);
      
      if (userData) {
        setUser(userData);
      } else {
        // Decode user data from token if not provided
        const decodedToken = jwtDecode(token);
        setUser({
          id: decodedToken.sub || decodedToken.user_id,
          email: decodedToken.email,
          name: decodedToken.name || decodedToken.given_name,
          picture: decodedToken.picture,
        });
      }
    } catch (error) {
      console.error('Error during login:', error);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('authToken');
  };

  const isAuthenticated = () => {
    return !!user && !!token;
  };

  const getAuthHeaders = () => {
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    isAuthenticated,
    getAuthHeaders,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
