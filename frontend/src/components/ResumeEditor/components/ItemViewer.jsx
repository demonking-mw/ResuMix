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
							{(() => {
								if (!item.titles || item.titles.length === 0) {
									return (
										<div className="title-row">
											<div className="title-left">
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
														className="editable-item-title title-primary"
														placeholder={getTitlePlaceholder(
															formattedTitles.row1.leftIndex
														)}
														// Future: Add onChange handler
														// Note: For augmented titles, this only edits the first part
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
															className="editable-item-title title-secondary"
															placeholder={getTitlePlaceholder(
																formattedTitles.row1.rightIndex
															)}
															// Future: Add onChange handler
														/>
													) : (
														<span className="title-display title-secondary">
															{formattedTitles.row1.right}
														</span>
													)}
												</div>
											)}
										</div>

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
															className="editable-item-title title-tertiary"
															placeholder={getTitlePlaceholder(
																formattedTitles.row2.leftIndex
															)}
															// Future: Add onChange handler
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
																className="editable-item-title title-quaternary"
																placeholder={getTitlePlaceholder(
																	formattedTitles.row2.rightIndex
																)}
																// Future: Add onChange handler
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

										{/* Add title button for edit mode */}
										{mode === "edit" &&
											item.titles &&
											item.titles.length < 6 && (
												<button className="add-title-button" disabled>
													+ Add Title Field
												</button>
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
