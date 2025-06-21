import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import React from 'react';
import CreateProfile from './components/CreateProfile';
import Login from './components/Login';

export default function App() {
  // 'login' or 'signup'
  const [mode, setMode] = useState('login');

  return (
    <div className="App" style={{ padding: '2rem', textAlign: 'center' }}>
      {/* Toggle buttons */}
      <div style={{ marginBottom: '1.5rem' }}>
        <button
          onClick={() => setMode('login')}
          style={{
            marginRight: '1rem',
            padding: '0.5rem 1rem',
            background: mode === 'login' ? '#6366f1' : '#f0f0f0',
            color: mode === 'login' ? '#fff' : '#333',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Log In
        </button>
        <button
          onClick={() => setMode('signup')}
          style={{
            padding: '0.5rem 1rem',
            background: mode === 'signup' ? '#6366f1' : '#f0f0f0',
            color: mode === 'signup' ? '#fff' : '#333',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Sign Up
        </button>
      </div>

      {/* Render the chosen form */}
      {mode === 'login' ? <Login /> : <CreateProfile />}
    </div>
  );
}