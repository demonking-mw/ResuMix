// src/components/ResumeEditor/components/ParameterControls.jsx
import React from "react";

const ParameterControls = ({
  cateScores,
  mode,
  onUpdateWeight,
  onUpdateBias,
}) => {
  if (!cateScores) {
    return (
      <div className="parameter-controls">
        <div className="parameter-placeholder">
          <p>No parameters available</p>
        </div>
      </div>
    );
  }

  const { weight = 1, bias = 0 } = cateScores;

  // Helper function to get visual indicator for weight
  const getWeightIndicator = (weightValue) => {
    if (weightValue > 1.2) return "🔥"; // High priority
    if (weightValue > 1.0) return "⬆️"; // Above normal
    if (weightValue === 1.0) return "➡️"; // Normal
    if (weightValue > 0.5) return "⬇️"; // Below normal
    return "❄️"; // Low priority
  };

  // Helper function to get visual indicator for bias
  const getBiasIndicator = (biasValue) => {
    if (biasValue > 0.5) return "📈"; // Positive bias
    if (biasValue > 0) return "📊"; // Slight positive
    if (biasValue === 0) return "⚖️"; // Neutral
    if (biasValue > -0.5) return "📉"; // Slight negative
    return "📉"; // Negative bias
  };

  return (
    <div className="parameter-controls">
      <div className="parameter-header">
        <h4>Item Parameters</h4>
      </div>

      <div className="parameter-grid">
        {/* Weight Parameter */}
        <div className="parameter-item">
          <div className="parameter-label">
            <span className="parameter-name">Weight</span>
            <span className="parameter-indicator">
              {getWeightIndicator(weight)}
            </span>
          </div>

          {mode === "edit" ? (
            <div className="parameter-input-container">
              <input
                type="number"
                value={weight}
                step="0.01"
                min="0"
                max="2"
                className="parameter-input"
                onChange={(e) =>
                  onUpdateWeight(parseFloat(e.target.value) || 0)
                }
              />
              <div className="parameter-range">
                <input
                  type="range"
                  value={weight}
                  step="0.01"
                  min="0"
                  max="2"
                  className="parameter-slider"
                  onChange={(e) => onUpdateWeight(parseFloat(e.target.value))}
                />
              </div>
            </div>
          ) : (
            <div className="parameter-display">
              <span className="parameter-value">{weight}</span>
              <div className="parameter-bar">
                <div
                  className="parameter-fill weight-fill"
                  style={{
                    width: `${Math.max(0, Math.min(100, (weight / 2) * 100))}%`,
                  }}
                ></div>
              </div>
            </div>
          )}
        </div>

        {/* Bias Parameter */}
        <div className="parameter-item">
          <div className="parameter-label">
            <span className="parameter-name">Bias</span>
            <span className="parameter-indicator">
              {getBiasIndicator(bias)}
            </span>
          </div>

          {mode === "edit" ? (
            <div className="parameter-input-container">
              <input
                type="number"
                value={bias}
                step="0.01"
                min="-2"
                max="2"
                className="parameter-input"
                onChange={(e) => onUpdateBias(parseFloat(e.target.value) || 0)}
              />
              <div className="parameter-range">
                <input
                  type="range"
                  value={bias}
                  step="0.01"
                  min="-2"
                  max="2"
                  className="parameter-slider"
                  onChange={(e) => onUpdateBias(parseFloat(e.target.value))}
                />
              </div>
            </div>
          ) : (
            <div className="parameter-display">
              <span className="parameter-value">{bias}</span>
              <div className="parameter-bar">
                <div
                  className="parameter-fill bias-fill"
                  style={{
                    width: `${Math.max(
                      0,
                      Math.min(100, ((bias + 2) / 4) * 100)
                    )}%`,
                  }}
                ></div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ParameterControls;
