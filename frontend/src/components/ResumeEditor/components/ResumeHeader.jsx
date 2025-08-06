import React from "react";

// Helper function to strip HTML-like tags for display
const stripMarkupTags = (text) => {
	if (!text) return "";
	// Remove HTML-like tags but preserve the text content
	return text.replace(/<[^>]*>/g, "");
};

const ResumeHeader = ({ headingInfo, mode, onUpdate }) => {
	// Ensure we have a valid headingInfo object
	const safeHeadingInfo = headingInfo || {
		heading_name: "",
		subsequent_content: [],
	};

	// Handle adding new contact info
	const handleAddContact = () => {
		console.log("Add contact button clicked!");
		if (onUpdate) {
			const updatedHeader = {
				...safeHeadingInfo,
				subsequent_content: [
					...(safeHeadingInfo.subsequent_content || []),
					"", // Add empty contact field
				],
			};
			console.log("Updating header with new contact:", updatedHeader);
			onUpdate(updatedHeader);
		} else {
			console.log("No onUpdate handler provided");
		}
	};

	// Handle updating contact info
	const handleContactChange = (index, value) => {
		if (onUpdate) {
			const updatedContacts = [...(safeHeadingInfo.subsequent_content || [])];
			updatedContacts[index] = value;
			const updatedHeader = {
				...safeHeadingInfo,
				subsequent_content: updatedContacts,
			};
			onUpdate(updatedHeader);
		}
	};

	// Handle updating name
	const handleNameChange = (value) => {
		if (onUpdate) {
			const updatedHeader = {
				...safeHeadingInfo,
				heading_name: value,
			};
			onUpdate(updatedHeader);
		}
	};

	// Only show placeholder in view mode when there's no data
	if (!headingInfo && mode !== "edit") {
		return (
			<div className="resume-header">
				<div className="header-placeholder">
					<p>No header information available</p>
				</div>
			</div>
		);
	}

	return (
		<div className="resume-header">
			<div className="header-content">
				{/* Main name */}
				<div className="header-name">
					{mode === "edit" ? (
						<input
							type="text"
							value={safeHeadingInfo.heading_name || ""}
							className="editable-name"
							placeholder="Your Name"
							onChange={(e) => handleNameChange(e.target.value)}
						/>
					) : (
						<h1 className="name-display">
							{safeHeadingInfo.heading_name || "Name Not Provided"}
						</h1>
					)}
				</div>

				{/* Contact information */}
				<div className="header-contact">
					{safeHeadingInfo.subsequent_content?.map((contactItem, index) => (
						<div key={index} className="contact-item">
							{mode === "edit" ? (
								<input
									type="text"
									value={contactItem || ""}
									className="editable-contact"
									placeholder={`Contact info ${index + 1}`}
									onChange={(e) => handleContactChange(index, e.target.value)}
								/>
							) : (
								<span className="contact-display">
									{mode === "view" || mode === "parameters-only"
										? stripMarkupTags(contactItem)
										: contactItem}
								</span>
							)}
						</div>
					))}
				</div>
			</div>

			{/* Edit controls */}
			{mode === "edit" && (
				<div className="header-controls">
					<button
						className="add-contact-button"
						onClick={handleAddContact}
						onMouseDown={() => console.log("Button mouse down")}
						onMouseUp={() => console.log("Button mouse up")}
						style={{ pointerEvents: "auto", zIndex: 10 }}
					>
						+ Add Contact Info
					</button>
				</div>
			)}
		</div>
	);
};

export default ResumeHeader;
