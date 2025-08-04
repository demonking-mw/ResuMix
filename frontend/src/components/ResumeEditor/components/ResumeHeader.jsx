// src/components/ResumeEditor/components/ResumeHeader.jsx
import React from "react";

const ResumeHeader = ({ headingInfo, mode, onUpdate }) => {
	if (!headingInfo) {
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
							value={headingInfo.heading_name || ""}
							className="editable-name"
							placeholder="Your Name"
							onChange={(e) => {
								// Future: Handle name changes
								console.log("Name changed to:", e.target.value);
							}}
						/>
					) : (
						<h1 className="name-display">
							{headingInfo.heading_name || "Name Not Provided"}
						</h1>
					)}
				</div>

				{/* Contact information */}
				<div className="header-contact">
					{headingInfo.subsequent_content?.map((contactItem, index) => (
						<div key={index} className="contact-item">
							{mode === "edit" ? (
								<input
									type="text"
									value={contactItem || ""}
									className="editable-contact"
									placeholder={`Contact info ${index + 1}`}
									onChange={(e) => {
										// Future: Handle contact changes
										console.log(`Contact ${index} changed to:`, e.target.value);
									}}
								/>
							) : (
								<span className="contact-display">{contactItem}</span>
							)}
						</div>
					))}
				</div>
			</div>

			{/* Future: Add edit controls */}
			{mode === "edit" && (
				<div className="header-controls">
					<button className="add-contact-button" disabled>
						+ Add Contact Info
					</button>
				</div>
			)}
		</div>
	);
};

export default ResumeHeader;
