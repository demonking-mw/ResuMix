import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";

import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Landing from "./components/Landing";
import Login from "./components/Login";
import CreateProfile from "./components/CreateProfile";
import AccountHome from "./components/AccountHome";
import MasterResume from "./components/MasterResume";
import ResumeForm from "./input_components/ResumeForm";
import UILibraryDemo from "./components/UILibraryDemo";
import Optimize from "./components/Optimize";

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
					<Route
						path="/account"
						element={
							<ProtectedRoute>
								<AccountHome />
							</ProtectedRoute>
						}
					/>

					{/* 5) Master Resume Editor - New resume viewing/editing component */}
					<Route
						path="/master-resume"
						element={
							<ProtectedRoute>
								<MasterResume />
							</ProtectedRoute>
						}
					/>

					{/* 5b) Legacy Resume Form - Keeping for reference */}
					<Route
						path="/resume-form"
						element={
							<ProtectedRoute>
								<ResumeForm />
							</ProtectedRoute>
						}
					/>

					{/* 6) Optimize page - Generate tailored resumes */}
					<Route
						path="/optimize"
						element={
							<ProtectedRoute>
								<Optimize />
							</ProtectedRoute>
						}
					/>

					{/* 7) UI Library Demo */}
					<Route path="/demo" element={<UILibraryDemo />} />

					{/* 8) Fallback: redirect unknown URLs back to landing */}
					<Route path="*" element={<Navigate to="/" replace />} />
				</Routes>
			</BrowserRouter>
		</AuthProvider>
	);
}
