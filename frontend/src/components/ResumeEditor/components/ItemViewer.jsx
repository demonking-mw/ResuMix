// src/components/ResumeEditor/components/ItemViewer.jsx
import React, { useRef, useEffect } from "react";
import LineViewer from "./LineViewer";
import ParameterControls from "./ParameterControls";

const ItemViewer = ({
	item,
	itemIndex,
	sectionIndex,
	mode,
	showParameters,
	onUpdateTitles,
	onAddTitle,
	onRemoveLastTitle,
	onUpdateLineContent,
	onUpdateParameters,
	onAddNewLine,
	onDeleteLine,
	onDeleteItem,
}) => {
	const textareaRef = useRef(null);

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

	// Auto-resize textarea function
	const autoResizeTextarea = (textarea) => {
		if (textarea) {
			textarea.style.height = "auto";
			textarea.style.height = textarea.scrollHeight + "px";
		}
	};

	// Auto-resize on content change
	useEffect(() => {
		if (textareaRef.current && isCompactItem && mode === "edit") {
			autoResizeTextarea(textareaRef.current);
		}
	}, [
		item.lines?.[0]?.content_str,
		item.lines?.[0]?.content,
		isCompactItem,
		mode,
	]);

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

	// Format titles based on your backend logic from item_builder()
	const formatTitles = (titles) => {
		if (!titles || titles.length === 0) return null;

		const titleCount = titles.length;

		// Helper function to create augmented title (title1 | title2)
		const createAugmentedTitle = (main, secondary) => (
			<>
				{main}
				<span className="title-separator"> | </span>
				<span className="title-secondary">{secondary}</span>
			</>
		);

		if (titleCount === 1 || titleCount === 2 || titleCount === 4) {
			// Simple layout: para1 para2 / para3 para4
			return {
				row1: {
					left: titles[0],
					right: titleCount === 1 ? null : titles[1],
					leftIndex: 0,
					rightIndex: titleCount === 1 ? null : 1,
				},
				row2:
					titleCount === 4
						? {
								left: titles[2],
								right: titles[3],
								leftIndex: 2,
								rightIndex: 3,
						  }
						: null,
			};
		} else if (titleCount === 3 || titleCount === 5 || titleCount === 6) {
			// Augmented layout: (title1 | title2) title3 / ...
			const row1 = {
				left: createAugmentedTitle(titles[0], titles[1]),
				right: titles[2],
				leftIndex: 0,
				rightIndex: 2,
				leftSecondaryIndex: 1, // For the augmented part
			};

			let row2 = null;
			if (titleCount === 5) {
				row2 = {
					left: titles[3],
					right: titles[4],
					leftIndex: 3,
					rightIndex: 4,
				};
			} else if (titleCount === 6) {
				row2 = {
					left: createAugmentedTitle(titles[3], titles[4]),
					right: titles[5],
					leftIndex: 3,
					rightIndex: 5,
					leftSecondaryIndex: 4,
				};
			}

			return { row1, row2 };
		}

		return null;
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
								ref={textareaRef}
								value={
									item.lines[0]?.content_str || item.lines[0]?.content || ""
								}
								className="editable-compact-line"
								placeholder="Enter content..."
								onChange={(e) => {
									// Update the first (and only) line content
									onUpdateLineContent(0, e.target.value);
									// Auto-resize the textarea
									autoResizeTextarea(e.target);
								}}
								onInput={(e) => {
									// Additional auto-resize on input
									autoResizeTextarea(e.target);
								}}
							/>
						) : (
							<span className="compact-text">
								{item.lines[0]?.content_str ||
									item.lines[0]?.content ||
									"No content"}
							</span>
						)}
					</div>
					{/* Delete button beneath the text in edit mode */}
					{mode === "edit" && (
						<button
							className="item-delete-button-compact"
							onClick={onDeleteItem}
							title="Delete this item"
						>
							× Remove
						</button>
					)}
				</div>
			) : (
				<>
					{/* Standard Item Layout with Titles */}
					<div className="item-header">
						{/* Delete button in edit mode */}

						<div className="item-titles">
							{(() => {
								if (!item.titles || item.titles.length === 0) {
									return (
										<div className="no-titles-section">
											<div className="title-row">
												<div className="title-left">
													{mode === "edit" ? (
														<input
															type="text"
															value=""
															className="item-title-input"
															placeholder="Item Title"
															onChange={(e) =>
																onUpdateTitles(0, e.target.value)
															}
														/>
													) : (
														<span className="title-display">Untitled Item</span>
													)}
												</div>
											</div>
											{/* Add title button for items with no titles */}
											{mode === "edit" && (
												<div className="title-button-group">
													<button
														className="add-title-button"
														onClick={onAddTitle}
													>
														+ Add Title Field
													</button>
													{/* Only show remove button if there are titles to remove */}
													{item.titles && item.titles.length > 0 && (
														<button
															className="remove-title-button"
															onClick={onRemoveLastTitle}
														>
															- Remove Last Title
														</button>
													)}
												</div>
											)}
										</div>
									);
								}

								const formattedTitles = formatTitles(item.titles);
								if (!formattedTitles) return null;

								return (
									<div className="formatted-titles">
										{/* First Row */}
										<div className="title-row title-row-1">
											<div className="title-left">
												{mode === "edit" ? (
													<input
														type="text"
														value={
															item.titles[formattedTitles.row1.leftIndex] || ""
														}
														className="item-title-input"
														placeholder={getTitlePlaceholder(
															formattedTitles.row1.leftIndex
														)}
														onChange={(e) =>
															onUpdateTitles(
																formattedTitles.row1.leftIndex,
																e.target.value
															)
														}
													/>
												) : (
													<span className="title-display title-primary">
														{formattedTitles.row1.left}
													</span>
												)}
											</div>

											{formattedTitles.row1.right && (
												<div className="title-right">
													{mode === "edit" ? (
														<input
															type="text"
															value={
																item.titles[formattedTitles.row1.rightIndex] ||
																""
															}
															className="item-title-input"
															placeholder={getTitlePlaceholder(
																formattedTitles.row1.rightIndex
															)}
															onChange={(e) =>
																onUpdateTitles(
																	formattedTitles.row1.rightIndex,
																	e.target.value
																)
															}
														/>
													) : (
														<span className="title-display title-secondary">
															{formattedTitles.row1.right}
														</span>
													)}
												</div>
											)}
										</div>

										{/* Secondary title row for edit mode (centered below) */}
										{mode === "edit" &&
											formattedTitles.row1.leftSecondaryIndex !== undefined && (
												<div className="title-row title-row-secondary">
													<div className="title-center">
														<input
															type="text"
															value={
																item.titles[
																	formattedTitles.row1.leftSecondaryIndex
																] || ""
															}
															className="item-title-input"
															placeholder={getTitlePlaceholder(
																formattedTitles.row1.leftSecondaryIndex
															)}
															onChange={(e) =>
																onUpdateTitles(
																	formattedTitles.row1.leftSecondaryIndex,
																	e.target.value
																)
															}
														/>
													</div>
												</div>
											)}

										{/* Second Row (if needed) */}
										{formattedTitles.row2 && (
											<div className="title-row title-row-2">
												<div className="title-left">
													{mode === "edit" ? (
														<input
															type="text"
															value={
																item.titles[formattedTitles.row2.leftIndex] ||
																""
															}
															className="item-title-input"
															placeholder={getTitlePlaceholder(
																formattedTitles.row2.leftIndex
															)}
															onChange={(e) =>
																onUpdateTitles(
																	formattedTitles.row2.leftIndex,
																	e.target.value
																)
															}
														/>
													) : (
														<span className="title-display title-tertiary">
															{formattedTitles.row2.left}
														</span>
													)}
												</div>
												{formattedTitles.row2.right && (
													<div className="title-right">
														{mode === "edit" ? (
															<input
																type="text"
																value={
																	item.titles[
																		formattedTitles.row2.rightIndex
																	] || ""
																}
																className="item-title-input"
																placeholder={getTitlePlaceholder(
																	formattedTitles.row2.rightIndex
																)}
																onChange={(e) =>
																	onUpdateTitles(
																		formattedTitles.row2.rightIndex,
																		e.target.value
																	)
																}
															/>
														) : (
															<span className="title-display title-quaternary">
																{formattedTitles.row2.right}
															</span>
														)}
													</div>
												)}
											</div>
										)}

										{/* Add/Remove title buttons for edit mode */}
										{mode === "edit" && (
											<div className="title-button-group">
												{/* Add title button - only show if less than 6 titles */}
												{item.titles &&
													item.titles.length > 0 &&
													item.titles.length < 6 && (
														<button
															className="add-title-button"
															onClick={onAddTitle}
														>
															+ Add Title Field
														</button>
													)}
												{/* Remove title button - only show if there are titles to remove */}
												{item.titles && item.titles.length > 0 && (
													<button
														className="remove-title-button"
														onClick={onRemoveLastTitle}
													>
														- Remove Last Title
													</button>
												)}
											</div>
										)}
									</div>
								);
							})()}
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
								<button
									className="item-delete-button"
									onClick={onDeleteItem}
									title="Delete this item"
								>
									×
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
										onUpdateContent={(newContent) =>
											onUpdateLineContent(lineIndex, newContent)
										}
										onDeleteLine={() => onDeleteLine(lineIndex)}
									/>
								))}
								{/* Add line button for edit mode */}
								{mode === "edit" && (
									<div className="add-line-container">
										<button
											className="edit-button add-button"
											onClick={onAddNewLine}
										>
											+ Add Line
										</button>
									</div>
								)}
							</div>
						) : (
							<div className="empty-item">
								<p className="empty-message">No content lines</p>
								{mode === "edit" && (
									<button
										className="edit-button add-button"
										onClick={onAddNewLine}
									>
										+ Add Line
									</button>
								)}
							</div>
						)}
					</div>
				</>
			)}

			{/* Parameter Controls - Always show for both compact and standard */}
			{showParameters && (
				<ParameterControls
					cateScores={item.cate_scores}
					mode={mode}
					onUpdateWeight={(value) => onUpdateParameters("weight", value)}
					onUpdateBias={(value) => onUpdateParameters("bias", value)}
				/>
			)}
		</div>
	);
};

export default ItemViewer;
