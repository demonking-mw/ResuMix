// src/components/MasterResume/MasterResume.jsx
import React, { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import ResumeEditor from "../ResumeEditor";
import NavBar from "../NavBar";
import "./MasterResume.css";

const MasterResume = () => {
	const navigate = useNavigate();
	const { user } = useAuth();
	const [searchParams, setSearchParams] = useSearchParams();
	const [currentMode, setCurrentMode] = useState("view");

	// Check URL parameters for mode on component mount
	useEffect(() => {
		const modeParam = searchParams.get("mode");
		if (
			modeParam &&
			["view", "edit", "parameters-only", "view-latex"].includes(modeParam)
		) {
			setCurrentMode(modeParam);
		}
	}, [searchParams]);

	// Demo: Toggle between different modes for testing
	const handleModeChange = (newMode) => {
		setCurrentMode(newMode);
		// Update URL parameter when mode changes
		const newSearchParams = new URLSearchParams(searchParams);
		newSearchParams.set("mode", newMode);
		setSearchParams(newSearchParams);
	};

	return (
		<div className="master-resume-container">
			<NavBar />

			{/* Page Header */}
			<div className="master-resume-header">
				<div className="header-content">
					<div className="header-left">
						<button
							className="nav-btn secondary"
							onClick={() => navigate("/account")}
						>
							← Back to Dashboard
						</button>
					</div>

					<div className="header-text">
						<h1>Master Resume</h1>
						<p className="header-subtitle">
							View and edit your comprehensive resume template
						</p>
					</div>

					<div className="header-right">
						<button
							className="nav-btn primary"
							onClick={() => navigate("/optimize")}
						>
							Generate Resume →
						</button>
					</div>
				</div>

				{/* Mode Controls - For Testing */}
				<div className="mode-controls">
					<div className="mode-buttons">
						<button
							className={`mode-btn ${currentMode === "view" ? "active" : ""}`}
							onClick={() => handleModeChange("view")}
						>
							👁️ View Mode
						</button>
						<button
							className={`mode-btn ${currentMode === "edit" ? "active" : ""}`}
							onClick={() => handleModeChange("edit")}
						>
							✏️ Edit Mode
						</button>
						<button
							className={`mode-btn ${
								currentMode === "parameters-only" ? "active" : ""
							}`}
							onClick={() => handleModeChange("parameters-only")}
						>
							📄 Parameters Only
						</button>
						<button
							className={`mode-btn ${
								currentMode === "view-latex" ? "active" : ""
							}`}
							onClick={() => handleModeChange("view-latex")}
						>
							View LaTeX
						</button>
					</div>
				</div>
			</div>

			{/* Main Resume Editor */}
			<div className="resume-editor-wrapper">
				<ResumeEditor
					mode={currentMode}
					showParameters={currentMode !== "view" || true} // Always show parameters for now
					showContent={currentMode !== "parameters-only"}
				/>
			</div>
		</div>
	);
};

export default MasterResume;
