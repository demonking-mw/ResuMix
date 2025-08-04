// src/components/ResumeEditor/components/ItemViewer.jsx
import React from "react";
import LineViewer from "./LineViewer";
import ParameterControls from "./ParameterControls";

const ItemViewer = ({
	item,
	itemIndex,
	sectionIndex,
	mode,
	showParameters,
	onUpdate,
}) => {
	if (!item) {
		return (
			<div className="item-viewer">
				<div className="item-placeholder">
					<p>Item data not available</p>
				</div>
			</div>
		);
	}

	// Determine if this is a compact item (single line with no meaningful titles)
	const hasNoTitles =
		!item.titles ||
		item.titles.length === 0 ||
		item.titles.every((title) => !title || title.trim() === "");
	const hasSingleLine = item.lines && item.lines.length === 1;
	const isCompactItem = hasNoTitles && hasSingleLine;

	// Get title placeholders based on index
	const getTitlePlaceholder = (index) => {
		const placeholders = [
			"Job Title/Position",
			"Company/Organization",
			"Date Range",
			"Location",
			"Additional Info",
			"Extra Details",
		];
		return placeholders[index] || `Title ${index + 1}`;
	};

	return (
		<div
			className={`item-viewer ${
				isCompactItem ? "item-compact" : "item-standard"
			}`}
		>
			{/* Compact Display for Single-Line Items (like Skills) */}
			{isCompactItem ? (
				<div className="item-compact-content">
					<div className="compact-line">
						{mode === "edit" ? (
							<textarea
								value={
									item.lines[0]?.content_str || item.lines[0]?.content || ""
								}
								className="editable-compact-line"
								placeholder="Enter content..."
								rows={1}
								// Future: Add onChange handler
							/>
						) : (
							<span className="compact-text">
								{item.lines[0]?.content_str ||
									item.lines[0]?.content ||
									"No content"}
							</span>
						)}
					</div>
				</div>
			) : (
				<>
					{/* Standard Item Layout with Titles */}
					<div className="item-header">
						<div className="item-titles">
							{item.titles && item.titles.length > 0 ? (
								item.titles.map((title, titleIndex) => (
									<div
										key={titleIndex}
										className={`item-title item-title-${titleIndex}`}
									>
										{mode === "edit" ? (
											<input
												type="text"
												value={title || ""}
												className="editable-item-title"
												placeholder={getTitlePlaceholder(titleIndex)}
												// Future: Add onChange handler
											/>
										) : (
											<span className="title-display">{title}</span>
										)}
									</div>
								))
							) : (
								<div className="item-title">
									{mode === "edit" ? (
										<input
											type="text"
											value=""
											className="editable-item-title"
											placeholder="Item Title"
											// Future: Add onChange handler
										/>
									) : (
										<span className="title-display">Untitled Item</span>
									)}
								</div>
							)}

							{/* Add title button for edit mode */}
							{mode === "edit" && item.titles && item.titles.length < 6 && (
								<button className="add-title-button" disabled>
									+ Add Title Field
								</button>
							)}
						</div>

						{/* Item metadata */}
						<div className="item-metadata">
							<span className="item-style">
								Style: {item.aux_info?.style || "n"}
							</span>
							<span className="item-type">
								Type: {isCompactItem ? "Compact" : "Standard"}
							</span>
						</div>

						{/* Future: Item controls for edit mode */}
						{mode === "edit" && (
							<div className="item-controls">
								<button className="move-up-button" disabled>
									↑
								</button>
								<button className="move-down-button" disabled>
									↓
								</button>
								<button className="delete-item-button" disabled>
									🗑
								</button>
							</div>
						)}
					</div>

					{/* Item Content Lines */}
					<div className="item-content">
						{item.lines?.length > 0 ? (
							<div className="item-lines">
								{item.lines.map((line, lineIndex) => (
									<LineViewer
										key={lineIndex}
										line={line}
										lineIndex={lineIndex}
										itemIndex={itemIndex}
										sectionIndex={sectionIndex}
										mode={mode}
										onUpdate={(updatedLine) => {
											// Future: Handle line updates
											console.log("Line update:", updatedLine);
										}}
									/>
								))}
							</div>
						) : (
							<div className="empty-item">
								<p className="empty-message">No content lines</p>
								{mode === "edit" && (
									<button className="add-line-button" disabled>
										+ Add Line
									</button>
								)}
							</div>
						)}
					</div>

					{/* Add line button for edit mode */}
					{mode === "edit" && item.lines?.length > 0 && (
						<div className="item-footer">
							<button className="add-line-button" disabled>
								+ Add New Line
							</button>
						</div>
					)}
				</>
			)}

			{/* Parameter Controls - Always show for both compact and standard */}
			{showParameters && (
				<ParameterControls
					cateScores={item.cate_scores}
					mode={mode}
					onUpdate={(updatedScores) => {
						// Future: Handle parameter updates
						console.log("Parameter update:", updatedScores);
					}}
				/>
			)}
		</div>
	);
};

export default ItemViewer;
