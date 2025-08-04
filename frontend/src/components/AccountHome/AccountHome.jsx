// src/components/AccountHome/AccountHome.jsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import "./AccountHome.css";
import NavBar from "../NavBar";

const AccountHome = () => {
	const { user, logout, reauthToken, reauthenticate, userStatus } = useAuth();
	const navigate = useNavigate();
	const [showHelp, setShowHelp] = useState(null);
	const [hoveredStatus, setHoveredStatus] = useState(null);
	const [statusTimeout, setStatusTimeout] = useState(null);

	// Console log user's master resume object
	console.log(
		"👤 AccountHome - User's master resume object:",
		user?.resumeinfo
	);

	// Function to get color based on status value
	const getStatusColor = (status) => {
		switch (status) {
			case "r":
				return "#cc101c"; // red
			case "o":
				return "#EB6702"; // high contrast burnt orange warning
			case "y":
				return "#f0cc00"; // yellow
			case "g":
				return "#24D648"; // lighter green
			default:
				return "#6c757d"; // gray for unknown/null status
		}
	};

	// Function to get text color for contrast and emphasis
	const getTextColor = (status) => {
		switch (status) {
			case "r":
				return "#fff"; // white text on red (high contrast)
			case "o":
				return "#fff"; // white text on orange (high contrast)
			case "y":
				return "#000"; // black text on yellow (better contrast)
			case "g":
				return "#fff"; // white text on green (high contrast, emphasizes "good")
			default:
				return "#fff"; // white text on gray
		}
	};

	// Function to get detailed status messages for hover
	const getDetailedStatusMessage = (statusType, status) => {
		const messages = {
			resume_state: {
				r: "Master resume not created - Please create your resume",
				o: `Master resume set but only contain ${
					userStatus?.item_count || 0
				} lines - Adding more content will improve job-specific resume optimization`,
				y: `POGG (${userStatus?.item_count || 0} lines)`,
				g: `Master resume has ${
					userStatus?.item_count || 0
				} lines - Good to go!`,
				default: "Resume status unknown - Please check configuration",
			},
			tweak_status: {
				r: "Parameters not configured - Customize your parameters to emphasize key experiences.",
				o: "Partially tweaked - continue for better results",
				y: "Basic parameters set - Consider advanced options",
				g: "Parameters optimally configured for best results",
				default: "Parameter status unknown - Please check settings",
			},
			generate_status: {
				r: "Not ready - Please finish previous steps first",
				o: "Resume severely limited - Consider revisiting previous steps",
				y: "Mostly ready - Imperfections may occur",
				g: "ALL SET!",
				default: "Generation status unknown - Please check setup",
			},
		};

		return (
			messages[statusType]?.[status] ||
			messages[statusType]?.default ||
			"Status unknown"
		);
	};

	const handleStatusHoverEnter = (statusType) => {
		// Clear any existing timeout
		if (statusTimeout) {
			clearTimeout(statusTimeout);
			setStatusTimeout(null);
		}
		setHoveredStatus(statusType);
	};

	const handleStatusHoverLeave = () => {
		// Set a timeout to hide the status after 1 second
		const timeout = setTimeout(() => {
			setHoveredStatus(null);
			setStatusTimeout(null);
		}, 500);
		setStatusTimeout(timeout);
	};

	const handleLogout = () => {
		logout();
		navigate("/");
	};

	const handleCardClick = (destination) => {
		// TODO: Implement navigation logic
		console.log(`Navigating to: ${destination}`);
		navigate(destination);
	};

	const handleHelpClick = (e, stepNumber) => {
		e.stopPropagation(); // Prevent card click
		setShowHelp(showHelp === stepNumber ? null : stepNumber);
	};

	return (
		<div className="account-container">
			<NavBar />

			{/* Status Bar */}
			<div className="status-bar">
				<div className="status-content">
					<span className="status-text">STATUS BAR</span>
				</div>
			</div>

			{/* Main Content */}
			<main className="account-main">
				<div className="workflow-container">
					{/* Step 1: Master Resume */}
					<div className="workflow-step">
						<div className="status-indicator">
							<span
								className={`status-label ${
									hoveredStatus === "resume_state"
										? "status-label-expanded"
										: ""
								}`}
								style={{
									backgroundColor: getStatusColor(userStatus?.resume_state),
									color: getTextColor(userStatus?.resume_state),
								}}
								onMouseEnter={() => handleStatusHoverEnter("resume_state")}
								onMouseLeave={handleStatusHoverLeave}
							>
								{hoveredStatus === "resume_state"
									? getDetailedStatusMessage(
											"resume_state",
											userStatus?.resume_state
									  )
									: "<STATUS_INDICATOR>"}
							</span>
						</div>
						<div
							className="step-card clickable-card"
							onClick={() => handleCardClick("/master-resume")}
						>
							<div className="step-content">
								<span className="step-title">Set your master resume</span>
								<p className="step-description">
									Upload and configure your comprehensive resume template
								</p>
								<button
									className="step-button help-button"
									onClick={(e) => handleHelpClick(e, 1)}
								>
									Help
								</button>
							</div>
						</div>
					</div>

					{/* Step 2: Parameters */}
					<div className="workflow-step">
						<div className="status-indicator">
							<span
								className={`status-label ${
									hoveredStatus === "tweak_status"
										? "status-label-expanded"
										: ""
								}`}
								style={{
									backgroundColor: getStatusColor(userStatus?.tweak_status),
									color: getTextColor(userStatus?.tweak_status),
								}}
								onMouseEnter={() => handleStatusHoverEnter("tweak_status")}
								onMouseLeave={handleStatusHoverLeave}
							>
								{hoveredStatus === "tweak_status"
									? getDetailedStatusMessage(
											"tweak_status",
											userStatus?.tweak_status
									  )
									: "<STATUS_INDICATOR>"}
							</span>
						</div>
						<div
							className="step-card clickable-card"
							// onClick={() => handleCardClick("/parameters")}
						>
							<div className="step-content">
								<span className="step-title">
									Tweak your resume's parameter
								</span>
								<p className="step-description">
									Customize settings and preferences for resume optimization
								</p>
								<button
									className="step-button help-button"
									onClick={(e) => handleHelpClick(e, 2)}
								>
									Help
								</button>
							</div>
						</div>
					</div>

					{/* Step 3: Generate */}
					<div className="workflow-step">
						<div className="status-indicator">
							<span
								className={`status-label ${
									hoveredStatus === "generate_status"
										? "status-label-expanded"
										: ""
								}`}
								style={{
									backgroundColor: getStatusColor(userStatus?.generate_status),
									color: getTextColor(userStatus?.generate_status),
								}}
								onMouseEnter={() => handleStatusHoverEnter("generate_status")}
								onMouseLeave={handleStatusHoverLeave}
							>
								{hoveredStatus === "generate_status"
									? getDetailedStatusMessage(
											"generate_status",
											userStatus?.generate_status
									  )
									: "<STATUS_INDICATOR>"}
							</span>
						</div>
						<div
							className="step-card clickable-card"
							onClick={() => handleCardClick("/optimize")}
						>
							<div className="step-content">
								<span className="step-title">Generate</span>
								<p className="step-description">
									Create optimized resumes tailored to specific job
									opportunities
								</p>
								<button
									className="step-button help-button"
									onClick={(e) => handleHelpClick(e, 3)}
								>
									Help
								</button>
							</div>
						</div>
					</div>
				</div>

				{/* Help Information */}
				{showHelp && (
					<div className="help-section">
						<div className="help-content">
							<button
								className="help-close-button"
								onClick={() => setShowHelp(null)}
								aria-label="Close help"
							>
								×
							</button>
							{showHelp === 1 && (
								<div className="help-info">
									<h3>Master Resume Help</h3>
									<p>
										Upload your complete resume template that contains all your
										experience, skills, and achievements. This will serve as the
										foundation for generating tailored resumes.
									</p>
									<ul>
										<li>Upload PDF or Word document</li>
										<li>Include all relevant experience</li>
										<li>Add comprehensive skills list</li>
									</ul>
								</div>
							)}
							{showHelp === 2 && (
								<div className="help-info">
									<h3>Parameters Help</h3>
									<p>
										Configure settings that control how your resume is optimized
										for different job opportunities.
									</p>
									<ul>
										<li>Set keyword matching preferences</li>
										<li>Choose resume sections to prioritize</li>
										<li>Adjust optimization algorithms</li>
									</ul>
								</div>
							)}
							{showHelp === 3 && (
								<div className="help-info">
									<h3>Generate Help</h3>
									<p>
										Create customized resumes tailored to specific job postings
										using your master resume and configured parameters.
									</p>
									<ul>
										<li>Paste job description</li>
										<li>Select optimization level</li>
										<li>Download tailored resume</li>
									</ul>
								</div>
							)}
						</div>
					</div>
				)}
			</main>
		</div>
	);
};

export default AccountHome;
