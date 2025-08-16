import React from "react";
import "./ConfirmationModal.css";

const ConfirmationModal = ({
  isOpen,
  title,
  message,
  confirmText = "Delete",
  cancelText = "Cancel",
  onConfirm,
  onCancel,
  isDangerous = false,
}) => {
  if (!isOpen) return null;

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onCancel();
    }
  };

  return (
    <div className="confirmation-modal-backdrop" onClick={handleBackdropClick}>
      <div className="confirmation-modal">
        <div className="confirmation-modal-header">
          <h3 className="confirmation-modal-title">{title}</h3>
        </div>
        <div className="confirmation-modal-body">
          <p className="confirmation-modal-message">{message}</p>
        </div>
        <div className="confirmation-modal-footer">
          <button
            className="confirmation-modal-button cancel-button"
            onClick={onCancel}
          >
            {cancelText}
          </button>
          <button
            className={`confirmation-modal-button confirm-button ${
              isDangerous ? "dangerous" : ""
            }`}
            onClick={onConfirm}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationModal;
