// src/components/ResumeEditor/components/SectionViewer.jsx
import React from "react";
import ItemViewer from "./ItemViewer";

const SectionViewer = ({
	section,
	sectionIndex,
	mode,
	showParameters,
	onUpdate,
}) => {
	if (!section) {
		return (
			<div className="section-viewer">
				<div className="section-placeholder">
					<p>Section data not available</p>
				</div>
			</div>
		);
	}

	// Detect if this section is primarily compact items (like Skills)
	const compactItemsCount =
		section.items?.filter((item) => {
			const hasNoTitles =
				!item.titles ||
				item.titles.length === 0 ||
				item.titles.every((title) => !title || title.trim() === "");
			const hasSingleLine = item.lines && item.lines.length === 1;
			return hasNoTitles && hasSingleLine;
		}).length || 0;

	const totalItems = section.items?.length || 0;
	const isCompactSection =
		totalItems > 0 && compactItemsCount / totalItems > 0.7; // 70% or more are compact

	return (
		<div
			className={`section-viewer ${
				isCompactSection ? "compact-section" : "standard-section"
			}`}
		>
			{/* Section Header */}
			<div className="section-header">
				<div className="section-title-container">
					{mode === "edit" ? (
						<input
							type="text"
							value={section.title || ""}
							className="editable-section-title"
							placeholder="Section Title"
							// Future: Add onChange handler
						/>
					) : (
						<h2 className="section-title">
							{section.title || "Untitled Section"}
						</h2>
					)}
				</div>

				{/* Section metadata - visible in debug/dev mode */}
				<div className="section-metadata">
					<span className="section-id">ID: {section.sect_id}</span>
					<span className="section-stats">
						{totalItems} items ({compactItemsCount} compact)
					</span>
				</div>

				{/* Future: Section controls for edit mode */}
				{mode === "edit" && (
					<div className="section-controls">
						<button className="move-up-button" disabled>
							↑
						</button>
						<button className="move-down-button" disabled>
							↓
						</button>
						<button className="delete-section-button" disabled>
							🗑
						</button>
					</div>
				)}
			</div>

			{/* Section Items */}
			<div className="section-items">
				{section.items?.length > 0 ? (
					section.items.map((item, itemIndex) => (
						<ItemViewer
							key={itemIndex}
							item={item}
							itemIndex={itemIndex}
							sectionIndex={sectionIndex}
							mode={mode}
							showParameters={showParameters}
							onUpdate={(updatedItem) => {
								// Future: Handle item updates
								console.log("Item update:", updatedItem);
							}}
						/>
					))
				) : (
					<div className="empty-section">
						<p className="empty-message">No items in this section</p>
						{mode === "edit" && (
							<button className="add-item-button" disabled>
								+ Add Item
							</button>
						)}
					</div>
				)}
			</div>

			{/* Add item button for edit mode */}
			{mode === "edit" && section.items?.length > 0 && (
				<div className="section-footer">
					<button className="add-item-button" disabled>
						+ Add New Item
					</button>
				</div>
			)}
		</div>
	);
};

export default SectionViewer;
