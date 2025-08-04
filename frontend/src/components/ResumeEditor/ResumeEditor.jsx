// src/components/ResumeEditor/ResumeEditor.jsx
import React, { useState, useEffect } from "react";
import { useAuth } from "../../context/AuthContext";
import "./ResumeEditor.css";
import SectionViewer from "./components/SectionViewer";
import ResumeHeader from "./components/ResumeHeader";

const ResumeEditor = ({
	mode = "view", // "view", "edit", "parameters-only"
	showParameters = true,
	showContent = true,
	onSave = null,
}) => {
	const { user } = useAuth();
	const [resumeData, setResumeData] = useState(null);
	const [isLoading, setIsLoading] = useState(true);
	const [error, setError] = useState(null);

	// Load resume data from user context (as shown in AccountHome.jsx line 18)
	useEffect(() => {
		try {
			if (user?.resumeinfo) {
				setResumeData(user.resumeinfo);
				setIsLoading(false);
			} else {
				setError("No resume data found");
				setIsLoading(false);
			}
		} catch (err) {
			setError("Failed to load resume data");
			setIsLoading(false);
			console.error("Error loading resume data:", err);
		}
	}, [user]);

	// Future: This will handle resume updates when edit mode is implemented
	const handleResumeUpdate = (updatedData) => {
		setResumeData(updatedData);
		// Future: Call backend API to save changes
		if (onSave) {
			onSave(updatedData);
		}
	};

	// Loading state
	if (isLoading) {
		return (
			<div className="resume-editor-container">
				<div className="resume-editor-loading">
					<div className="loading-spinner"></div>
					<p>Loading resume...</p>
				</div>
			</div>
		);
	}

	// Error state
	if (error || !resumeData) {
		return (
			<div className="resume-editor-container">
				<div className="resume-editor-error">
					<h3>Unable to Load Resume</h3>
					<p>{error || "Resume data is not available"}</p>
					<button
						className="retry-button"
						onClick={() => window.location.reload()}
					>
						Retry
					</button>
				</div>
			</div>
		);
	}

	return (
		<div className="resume-editor-container">
			<div className="resume-editor-header">
				<h1>Resume Editor</h1>
				<div className="editor-mode-indicator">
					<span className={`mode-badge mode-${mode}`}>
						{mode === "view"
							? "View Mode"
							: mode === "edit"
							? "Edit Mode"
							: "Parameters Only"}
					</span>
				</div>
			</div>

			<div className="resume-editor-content">
				{/* Resume Header Section */}
				{showContent && (
					<ResumeHeader
						headingInfo={resumeData.heading_info}
						mode={mode}
						onUpdate={(updatedHeader) => {
							// Future: Handle header updates
							console.log("Header update:", updatedHeader);
						}}
					/>
				)}

				{/* Resume Sections */}
				{showContent && (
					<div className="resume-sections">
						{resumeData.sections?.map((section, sectionIndex) => (
							<SectionViewer
								key={section.sect_id || sectionIndex}
								section={section}
								sectionIndex={sectionIndex}
								mode={mode}
								showParameters={showParameters}
								onUpdate={(updatedSection) => {
									// Future: Handle section updates
									console.log("Section update:", updatedSection);
								}}
							/>
						))}
					</div>
				)}

				{/* Parameters-only view */}
				{mode === "parameters-only" && (
					<div className="parameters-only-view">
						<h2>Resume Parameters</h2>
						{resumeData.sections?.map((section, sectionIndex) => (
							<div
								key={section.sect_id || sectionIndex}
								className="section-parameters"
							>
								<h3>{section.title}</h3>
								{section.items?.map((item, itemIndex) => (
									<div key={itemIndex} className="item-parameters">
										<div className="item-titles">
											{item.titles?.join(" • ") || "Untitled Item"}
										</div>
										<div className="parameter-controls">
											<span>Weight: {item.cate_scores?.weight || 1}</span>
											<span>Bias: {item.cate_scores?.bias || 0}</span>
										</div>
									</div>
								))}
							</div>
						))}
					</div>
				)}
			</div>

			{/* Future: Add floating action buttons for edit/save operations */}
			{mode === "edit" && (
				<div className="resume-editor-actions">
					<button className="action-button save-button" disabled>
						Save Changes
					</button>
					<button className="action-button cancel-button" disabled>
						Cancel
					</button>
				</div>
			)}
		</div>
	);
};

export default ResumeEditor;
