// src/components/ResumeEditor/components/LineViewer.jsx
import React from "react";

const LineViewer = ({
	line,
	lineIndex,
	itemIndex,
	sectionIndex,
	mode,
	onUpdateContent,
	onDeleteLine,
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
							className="line-content-input"
							placeholder="Enter line content..."
							rows={2}
							onChange={(e) => onUpdateContent(e.target.value)}
						/>
						<div className="edit-actions line-edit-actions">
							<button
								className="edit-button delete-button"
								onClick={onDeleteLine}
								title="Delete this line"
							>
								× Delete
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
