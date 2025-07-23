import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import "./App.css";

import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Landing       from './components/Landing';
import Login         from './components/Login';
import CreateProfile from './components/CreateProfile';
import AccountHome   from './components/AccountHome';
import ResumeForm from "./input_components/ResumeForm";
import UILibraryDemo from './components/UILibraryDemo';

export default function App() {

  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* 1) Landing page at "/" */}
          <Route path="/" element={<Landing />} />

          {/* 2) Login page */}
          <Route path="/login" element={<Login />} />

          {/* 3) Signup / Create Profile */}
          <Route path="/signup" element={<CreateProfile />} />

          {/* 4) Account Home - Main dashboard after login */}
          <Route path="/account" element={
            <ProtectedRoute>
              <AccountHome />
            </ProtectedRoute>
          } />

          {/* 5) Protected Home - Resume form */}
          <Route path="/home" element={
            <ProtectedRoute>
              <ResumeForm />
            </ProtectedRoute>
          } />

          {/* 6) UI Library Demo */}
          <Route path="/demo" element={<UILibraryDemo />} />

          {/* 6) Fallback: redirect unknown URLs back to landing */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}