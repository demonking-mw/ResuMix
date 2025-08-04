// src/components/ResumeEditor/ResumeEditor.jsx
import React, { useState, useEffect } from "react";
import { useAuth } from "../../context/AuthContext";
import api from "../../api/connection";
import "./ResumeEditor.css";
import SectionViewer from "./components/SectionViewer";
import ResumeHeader from "./components/ResumeHeader";

const ResumeEditor = ({
	mode = "view", // "view", "edit", "parameters-only"
	showParameters = true,
	showContent = true,
	onSave = null,
}) => {
	const { user, loading: authLoading, reauthToken } = useAuth();
	const [resumeData, setResumeData] = useState(null);
	const [isLoading, setIsLoading] = useState(true);
	const [error, setError] = useState(null);
	const [isSaving, setIsSaving] = useState(false);
	const [saveMessage, setSaveMessage] = useState("");
	const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

	// Load resume data from user context (as shown in AccountHome.jsx line 18)
	useEffect(() => {
		console.log(
			"ResumeEditor useEffect - authLoading:",
			authLoading,
			"user:",
			user
		);
		console.log("User object keys:", user ? Object.keys(user) : "no user");
		console.log("user?.resumeinfo:", user?.resumeinfo);

		// Don't proceed if auth is still loading
		if (authLoading) {
			console.log("Auth still loading, waiting...");
			return;
		}

		try {
			if (user?.resumeinfo) {
				console.log("Found resume data, loading...");
				setResumeData(user.resumeinfo);
				setIsLoading(false);
			} else {
				console.log("No resume data found. User object:", user);
				setError("No resume data found");
				setIsLoading(false);
			}
		} catch (err) {
			setError("Failed to load resume data");
			setIsLoading(false);
			console.error("Error loading resume data:", err);
		}
	}, [user, authLoading]);

	// Manual save function - triggered by save button
	const handleSaveResume = async () => {
		if (!resumeData || !user?.id || !reauthToken) {
			console.error("Missing required data:", {
				resumeData: !!resumeData,
				uid: !!user?.id,
				reauth_jwt: !!reauthToken,
			});
			setSaveMessage("❌ Missing user authentication data");
			return;
		}

		try {
			setIsSaving(true);
			setSaveMessage("Caching vectors...");

			// Prepare payload according to backend requirements
			const payload = {
				uid: user.id,
				reauth_jwt: reauthToken,
				resumeinfo: resumeData,
			};

			const response = await api.post("/resume", payload);
			const data = response.data;

			if (data.status) {
				setSaveMessage("✅ Saved successfully");
				setHasUnsavedChanges(false); // Reset unsaved changes flag
				// Clear success message after 3 seconds
				setTimeout(() => setSaveMessage(""), 3000);
				return data;
			} else {
				const detail = data.detail?.status || data.message || "Unknown error";
				setSaveMessage(`❌ Save failed: ${detail}`);
				console.error("Save failed:", detail);
				throw new Error(detail);
			}
		} catch (err) {
			console.error("Resume save error:", err);
			// Check if it's an axios error with response
			if (err.response && err.response.data) {
				const detail =
					err.response.data.detail?.status ||
					err.response.data.message ||
					"Server error";
				setSaveMessage(`❌ Save failed: ${detail}`);
			} else {
				setSaveMessage("❌ Network error — please try again later.");
			}
			throw err;
		} finally {
			setIsSaving(false);
		}
	};

	// Resume update handler - no auto-save, just update state
	const handleResumeUpdate = (updatedData) => {
		setResumeData(updatedData);
		setHasUnsavedChanges(true);
		// Call external onSave callback if provided
		if (onSave) {
			onSave(updatedData);
		}
	};

	// Deep clone helper for immutable updates
	const deepClone = (obj) => JSON.parse(JSON.stringify(obj));

	// Update section title
	const updateSectionTitle = (sectionIndex, newTitle) => {
		const updated = deepClone(resumeData);
		updated.sections[sectionIndex].title = newTitle;
		handleResumeUpdate(updated);
	};

	// Update item titles
	const updateItemTitles = (sectionIndex, itemIndex, titleIndex, newTitle) => {
		const updated = deepClone(resumeData);
		if (!updated.sections[sectionIndex].items[itemIndex].titles) {
			updated.sections[sectionIndex].items[itemIndex].titles = [];
		}
		updated.sections[sectionIndex].items[itemIndex].titles[titleIndex] =
			newTitle;
		handleResumeUpdate(updated);
	};

	// Update line content
	const updateLineContent = (
		sectionIndex,
		itemIndex,
		lineIndex,
		newContent
	) => {
		const updated = deepClone(resumeData);
		updated.sections[sectionIndex].items[itemIndex].lines[
			lineIndex
		].content_str = newContent;
		updated.sections[sectionIndex].items[itemIndex].lines[lineIndex].content =
			newContent;
		handleResumeUpdate(updated);
	};

	// Update item parameters
	const updateItemParameters = (sectionIndex, itemIndex, paramType, value) => {
		const updated = deepClone(resumeData);
		if (!updated.sections[sectionIndex].items[itemIndex].cate_scores) {
			updated.sections[sectionIndex].items[itemIndex].cate_scores = {
				weight: 1,
				bias: 0,
			};
		}
		updated.sections[sectionIndex].items[itemIndex].cate_scores[paramType] =
			value;
		handleResumeUpdate(updated);
	};

	// Add new section
	const addNewSection = () => {
		const updated = deepClone(resumeData);
		const newSection = {
			title: "NEW SECTION",
			sect_id: updated.sections.length,
			aux_info: { type: "section" },
			items: [],
		};
		updated.sections.push(newSection);
		handleResumeUpdate(updated);
	};

	// Delete section
	const deleteSection = (sectionIndex) => {
		const updated = deepClone(resumeData);
		updated.sections.splice(sectionIndex, 1);
		// Reindex section IDs
		updated.sections.forEach((section, index) => {
			section.sect_id = index;
		});
		handleResumeUpdate(updated);
	};

	// Add new item to section
	const addNewItem = (sectionIndex) => {
		const updated = deepClone(resumeData);
		const newItem = {
			titles: ["", "", ""],
			aux_info: { type: "items", style: "n" },
			cate_scores: { bias: 0, weight: 1 },
			lines: [],
		};
		updated.sections[sectionIndex].items.push(newItem);
		handleResumeUpdate(updated);
	};

	// Delete item from section
	const deleteItem = (sectionIndex, itemIndex) => {
		const updated = deepClone(resumeData);
		updated.sections[sectionIndex].items.splice(itemIndex, 1);
		handleResumeUpdate(updated);
	};

	// Add new line to item
	const addNewLine = (sectionIndex, itemIndex) => {
		const updated = deepClone(resumeData);
		const newLine = {
			content: "",
			content_str: "",
			aux_info: { type: "lines" },
		};
		updated.sections[sectionIndex].items[itemIndex].lines.push(newLine);
		handleResumeUpdate(updated);
	};

	// Delete line from item
	const deleteLine = (sectionIndex, itemIndex, lineIndex) => {
		const updated = deepClone(resumeData);
		updated.sections[sectionIndex].items[itemIndex].lines.splice(lineIndex, 1);
		handleResumeUpdate(updated);
	};

	// Loading state - show loading if auth is loading OR resume data is loading
	console.log(
		"ResumeEditor render - authLoading:",
		authLoading,
		"isLoading:",
		isLoading,
		"user:",
		!!user,
		"resumeData:",
		!!resumeData,
		"error:",
		error
	);

	if (authLoading || isLoading) {
		return (
			<div className="resume-editor-container">
				<div className="resume-editor-loading">
					<div className="loading-spinner"></div>
					<p>
						Loading resume... (auth: {authLoading ? "loading" : "done"}, data:{" "}
						{isLoading ? "loading" : "done"})
					</p>
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
		<div className="resume-editor-container" data-mode={mode}>
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
					{/* Save status indicator */}
					{(isSaving || saveMessage) && (
						<span
							className={`save-status ${
								isSaving
									? "saving"
									: saveMessage.includes("✅")
									? "success"
									: "error"
							}`}
						>
							{saveMessage}
						</span>
					)}
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
								onUpdateSectionTitle={(newTitle) =>
									updateSectionTitle(sectionIndex, newTitle)
								}
								onUpdateItemTitles={(itemIndex, titleIndex, newTitle) =>
									updateItemTitles(
										sectionIndex,
										itemIndex,
										titleIndex,
										newTitle
									)
								}
								onUpdateLineContent={(itemIndex, lineIndex, newContent) =>
									updateLineContent(
										sectionIndex,
										itemIndex,
										lineIndex,
										newContent
									)
								}
								onUpdateItemParameters={(itemIndex, paramType, value) =>
									updateItemParameters(
										sectionIndex,
										itemIndex,
										paramType,
										value
									)
								}
								onAddNewItem={() => addNewItem(sectionIndex)}
								onDeleteItem={(itemIndex) =>
									deleteItem(sectionIndex, itemIndex)
								}
								onAddNewLine={(itemIndex) =>
									addNewLine(sectionIndex, itemIndex)
								}
								onDeleteLine={(itemIndex, lineIndex) =>
									deleteLine(sectionIndex, itemIndex, lineIndex)
								}
								onDeleteSection={() => deleteSection(sectionIndex)}
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

			{/* Manual save button for edit mode */}
			{mode === "edit" && (
				<div className="resume-editor-actions">
					<button
						className={`action-button save-button ${
							hasUnsavedChanges ? "has-changes" : "no-changes"
						}`}
						onClick={handleSaveResume}
						disabled={isSaving || !hasUnsavedChanges}
					>
						{isSaving
							? "Saving..."
							: hasUnsavedChanges
							? "Save Changes *"
							: "No Changes"}
					</button>
					<button className="action-button cancel-button" disabled>
						Cancel
					</button>
				</div>
			)}

			{/* Add new section button for edit mode */}
			{mode === "edit" && (
				<div className="add-section-container">
					<button className="add-section-button" onClick={addNewSection}>
						+ Add New Section
					</button>
				</div>
			)}
		</div>
	);
};

export default ResumeEditor;
