import React from "react";
import "./HelpModal.css";

const HelpModal = ({ isOpen, title, content, onClose }) => {
	if (!isOpen) return null;

	const handleBackdropClick = (e) => {
		if (e.target === e.currentTarget) {
			onClose();
		}
	};

	return (
		<div className="help-modal-backdrop" onClick={handleBackdropClick}>
			<div className="help-modal">
				<div className="help-modal-header">
					<h3 className="help-modal-title">{title}</h3>
					<button className="help-modal-close" onClick={onClose}>
						×
					</button>
				</div>
				<div className="help-modal-content">{content}</div>
				<div className="help-modal-actions">
					<button className="help-modal-button" onClick={onClose}>
						Got it
					</button>
				</div>
			</div>
		</div>
	);
};

export default HelpModal;
