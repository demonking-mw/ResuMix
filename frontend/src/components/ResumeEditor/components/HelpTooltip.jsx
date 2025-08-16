import React, { useState } from "react";
import "./HelpTooltip.css";

const HelpTooltip = ({
  children,
  content,
  position = "bottom",
  className = "",
}) => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div
      className={`help-tooltip-container ${className}`}
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children}
      {isVisible && (
        <div className={`help-tooltip help-tooltip-${position}`}>
          <div className="help-tooltip-content">{content}</div>
        </div>
      )}
    </div>
  );
};

export default HelpTooltip;
