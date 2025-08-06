// src/components/ResumeEditor/components/SectionViewer.jsx
import React from "react";
import ItemViewer from "./ItemViewer";

const SectionViewer = ({
	section,
	sectionIndex,
	mode,
	showParameters,
	onUpdateSectionTitle,
	onUpdateItemTitles,
	onAddItemTitle,
	onRemoveLastItemTitle,
	onUpdateLineContent,
	onUpdateItemParameters,
	onAddNewItem,
	onDeleteItem,
	onAddNewLine,
	onDeleteLine,
	onDeleteSection,
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
							className="section-title-input"
							placeholder="Section Title"
							onChange={(e) => onUpdateSectionTitle(e.target.value)}
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

				{/* Section controls for edit mode */}
				{mode === "edit" && (
					<div className="edit-actions">
						<button
							className="edit-button add-button"
							onClick={onAddNewItem}
							title="Add new item to this section"
						>
							+ Add Item
						</button>
						<button
							className="edit-button delete-button"
							onClick={onDeleteSection}
							title="Delete this section"
						>
							Delete Section
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
							onUpdateTitles={(titleIndex, newTitle) =>
								onUpdateItemTitles(itemIndex, titleIndex, newTitle)
							}
							onAddTitle={() => onAddItemTitle(itemIndex)}
							onRemoveLastTitle={() => onRemoveLastItemTitle(itemIndex)}
							onUpdateLineContent={(lineIndex, newContent) =>
								onUpdateLineContent(itemIndex, lineIndex, newContent)
							}
							onUpdateParameters={(paramType, value) =>
								onUpdateItemParameters(itemIndex, paramType, value)
							}
							onAddNewLine={() => onAddNewLine(itemIndex)}
							onDeleteLine={(lineIndex) => onDeleteLine(itemIndex, lineIndex)}
							onDeleteItem={() => onDeleteItem(itemIndex)}
						/>
					))
				) : (
					<div className="empty-section">
						<p className="empty-message">No items in this section</p>
						{mode === "edit" && (
							<button className="edit-button add-button" onClick={onAddNewItem}>
								+ Add Item
							</button>
						)}
					</div>
				)}
			</div>
		</div>
	);
};

export default SectionViewer;
