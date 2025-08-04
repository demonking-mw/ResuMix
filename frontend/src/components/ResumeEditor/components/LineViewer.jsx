// src/components/ResumeEditor/components/LineViewer.jsx
import React from "react";

const LineViewer = ({
	line,
	lineIndex,
	itemIndex,
	sectionIndex,
	mode,
	onUpdate,
}) => {
	if (!line) {
		return (
			<div className="line-viewer">
				<div className="line-placeholder">
					<p>Line data not available</p>
				</div>
			</div>
		);
	}

	// Use content_str for display (clean version) or fall back to content
	const displayContent = line.content_str || line.content || "";

	return (
		<div className="line-viewer">
			<div className="line-content">
				{mode === "edit" ? (
					<div className="line-edit-container">
						<textarea
							value={displayContent}
							className="editable-line-content"
							placeholder="Enter line content..."
							rows={2}
							// Future: Add onChange handler
							// Should update both content (with formatting) and content_str (clean text)
							// onChange={(e) => onUpdate({...line, content_str: e.target.value, content: processFormatting(e.target.value)})}
						/>
						<div className="line-controls">
							<button className="move-up-button" disabled>
								↑
							</button>
							<button className="move-down-button" disabled>
								↓
							</button>
							<button className="delete-line-button" disabled>
								🗑
							</button>
						</div>
					</div>
				) : (
					<div className="line-display">
						<div className="line-bullet">•</div>
						<div className="line-text">{displayContent}</div>
						{/* Future: Show modification warning when edit functionality is implemented */}
						{/* Will need to track original_content or original_content_str for proper comparison */}
					</div>
				)}
			</div>
		</div>
	);
};

export default LineViewer;
