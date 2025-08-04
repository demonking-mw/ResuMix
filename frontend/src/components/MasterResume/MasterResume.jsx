// src/components/MasterResume/MasterResume.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import ResumeEditor from "../ResumeEditor";
import NavBar from "../NavBar";
import "./MasterResume.css";

const MasterResume = () => {
	const navigate = useNavigate();
	const { user } = useAuth();
	const [currentMode, setCurrentMode] = useState("view");

	// Demo: Toggle between different modes for testing
	const handleModeChange = (newMode) => {
		setCurrentMode(newMode);
	};

	return (
		<div className="master-resume-container">
			<NavBar />

			{/* Page Header */}
			<div className="master-resume-header">
				<div className="header-content">
					<h1>Master Resume Editor</h1>
					<p className="header-subtitle">
						View and edit your comprehensive resume template
					</p>
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
							⚙️ Parameters Only
						</button>
					</div>
				</div>

				{/* Navigation */}
				<div className="page-navigation">
					<button
						className="nav-btn secondary"
						onClick={() => navigate("/account")}
					>
						← Back to Dashboard
					</button>
					<button
						className="nav-btn primary"
						onClick={() => navigate("/optimize")}
					>
						Generate Resume →
					</button>
				</div>
			</div>

			{/* Debug Info - Shows current user data status */}
			<div className="debug-info">
				<div className="debug-content">
					<h3>🔍 Debug Information</h3>
					<div className="debug-grid">
						<div className="debug-item">
							<strong>User:</strong> {user?.user_name || "Not logged in"}
						</div>
						<div className="debug-item">
							<strong>Resume Data:</strong>{" "}
							{user?.resumeinfo ? "✅ Available" : "❌ Missing"}
						</div>
						<div className="debug-item">
							<strong>Sections:</strong>{" "}
							{user?.resumeinfo?.sections?.length || 0}
						</div>
						<div className="debug-item">
							<strong>Total Items:</strong>{" "}
							{user?.resumeinfo?.sections?.reduce(
								(total, section) => total + (section.items?.length || 0),
								0
							) || 0}
						</div>
						<div className="debug-item">
							<strong>Total Lines:</strong>{" "}
							{user?.resumeinfo?.sections?.reduce(
								(total, section) =>
									total +
									section.items?.reduce(
										(itemTotal, item) => itemTotal + (item.lines?.length || 0),
										0
									),
								0
							) || 0}
						</div>
						<div className="debug-item">
							<strong>Current Mode:</strong> {currentMode}
						</div>
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

			{/* Instructions Panel */}
			<div className="instructions-panel">
				<h3>📋 Testing Instructions</h3>
				<div className="instructions-content">
					<div className="instruction-section">
						<h4>View Mode (Current)</h4>
						<ul>
							<li>✅ Check if your resume data displays correctly</li>
							<li>✅ Verify all sections, items, and lines are visible</li>
							<li>✅ Review parameter values (weight/bias) for each item</li>
							<li>✅ Confirm header information is properly formatted</li>
						</ul>
					</div>

					<div className="instruction-section">
						<h4>Parameters Only Mode</h4>
						<ul>
							<li>⚙️ View only the weight/bias controls for each item</li>
							<li>⚙️ Useful for quick parameter adjustments</li>
							<li>⚙️ Compact view focusing on optimization settings</li>
						</ul>
					</div>

					<div className="instruction-section">
						<h4>Edit Mode (Future)</h4>
						<ul>
							<li>✏️ Will enable inline editing of all content</li>
							<li>✏️ Add/delete sections, items, and lines</li>
							<li>✏️ Adjust parameters with sliders and inputs</li>
							<li>✏️ Real-time saving to backend</li>
						</ul>
					</div>

					<div className="instruction-section">
						<h4>What to Test</h4>
						<ul>
							<li>🔍 Does your resume data load correctly?</li>
							<li>🎨 Is the layout clean and readable?</li>
							<li>📱 Does it work on mobile devices?</li>
							<li>⚡ Are the parameters displaying with correct values?</li>
							<li>🔄 Do mode switches work smoothly?</li>
							<li>
								🧩 Do sections with single-line items (like skills) display
								compactly?
							</li>
							<li>
								📝 Do sections with detailed items (like experience) use
								standard layout?
							</li>
						</ul>
					</div>
				</div>
			</div>
		</div>
	);
};

export default MasterResume;
