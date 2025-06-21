// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Landing       from './components/Landing';
import Login         from './components/Login';
import CreateProfile from './components/CreateProfile';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 1) Landing page at “/” */}
        <Route path="/" element={<Landing />} />

        {/* 2) Login page */}
        <Route path="/login" element={<Login />} />

        {/* 3) Signup / Create Profile */}
        <Route path="/signup" element={<CreateProfile />} />

        {/* 4) Placeholder Home after auth */}
        <Route path="/home" element={<h1>🏠 Home coming soon…</h1>} />

        {/* 5) Fallback: redirect unknown URLs back to landing */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}