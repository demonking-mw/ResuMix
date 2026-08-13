// src/components/Optimize/Optimize.jsx
import React, { useState, useEffect, useRef } from "react";
import { useAuth } from "../../context/AuthContext";
import api from "../../api/connection";
import "./Optimize.css";
import NavBar from "../NavBar";
import { Button, Textarea, Input } from "../../ui";

const RESUME_STATUS_TEXT = {
  r: "Add more items (fewer than 4)",
  o: "Usable, more items would help",
  g: "Good",
};

const TWEAK_STATUS_TEXT = {
  r: "Using default weights",
  o: "Partly tuned",
  g: "Tuned",
};

const Optimize = () => {
  const { user, getReauthHeaders, userStatus, reauthenticate } = useAuth();
  const [jobDescription, setJobDescription] = useState("");
  const [resumeName, setResumeName] = useState("");
  const [noCache, setNoCache] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [showTips, setShowTips] = useState(false);
  const [showTerminal, setShowTerminal] = useState(false);
  const [terminalMessages, setTerminalMessages] = useState([]);
  const reauthPerformed = useRef(false);

  // Reauthenticate only once on component mount
  useEffect(() => {
    const performReauth = async () => {
      if (!reauthPerformed.current) {
        reauthPerformed.current = true;
        // Perform reauthentication here if needed in the future
      }
    };
    performReauth();
  }, []); // Empty dependency array to run only once

  // Helper function to add messages to terminal
  const addTerminalMessage = (message, type = "info") => {
    const timestamp = new Date().toLocaleTimeString();
    setTerminalMessages((prev) => [...prev, { message, type, timestamp }]);
  };

  // Helper function to clear terminal
  const clearTerminal = () => {
    setTerminalMessages([]);
  };

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleGenerateResume = async () => {
    if (!jobDescription.trim()) {
      alert("Please enter a job description before generating your resume.");
      return;
    }

    // Show terminal and clear previous messages
    setShowTerminal(true);
    clearTerminal();
    setIsGenerating(true);

    try {
      addTerminalMessage("Starting resume generation process...", "info");

      // Step 1: Check generate_status
      addTerminalMessage("Checking system status...", "info");

      if (userStatus?.generate_status === "r") {
        addTerminalMessage("❌ Your master resume is empty", "error");
        addTerminalMessage(
          "Add at least one item with a bullet point under 'Set your master resume', then try again.",
          "error"
        );
        setIsGenerating(false);
        return;
      }

      addTerminalMessage("✅ System status check passed", "success");

      // Step 2: Reauthenticate
      addTerminalMessage("Authenticating user...", "info");
      const reauthSuccess = await reauthenticate();
      if (!reauthSuccess) {
        addTerminalMessage(
          "❌ Authentication failed. Please log in again.",
          "error"
        );
        setIsGenerating(false);
        return;
      }
      addTerminalMessage("✅ Authentication successful", "success");

      // Step 3: Prepare API call
      addTerminalMessage("Preparing resume generation request...", "info");
      const headers = getReauthHeaders();

      if (!headers.uid || !headers.reauth_jwt) {
        addTerminalMessage("❌ Missing authentication credentials", "error");
        setIsGenerating(false);
        return;
      }

      // Step 4: Call backend POST /resume/optimize endpoint
      addTerminalMessage(
        "Calling backend resume generation service...",
        "info"
      );

      // Use POST with data in request body instead of query parameters
      const response = await api.post(
        "/resume/optimize",
        {
          uid: headers.uid,
          reauth_jwt: headers.reauth_jwt,
          job_description: jobDescription,
          resume_name: resumeName.trim() || user?.user_name || "resume",
          no_cache: noCache, // boolean like backend expects
        },
        {
          responseType: "blob", // Critical for handling PDF binary data
        }
      );

      if (response.status === 200) {
        addTerminalMessage("✅ Resume generated successfully!", "success");
        addTerminalMessage("Downloading resume...", "info");

        // Handle file download - response.data should be a blob when responseType is 'blob'
        const blob = response.data;
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        const finalResumeName =
          resumeName.trim() || user?.user_name || "resume";
        a.style.display = "none";
        a.href = url;
        a.download = `${finalResumeName}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        addTerminalMessage("✅ Resume download completed!", "success");
      } else {
        addTerminalMessage(
          `❌ Failed to generate resume: ${response.status} ${response.statusText}`,
          "error"
        );
      }
    } catch (error) {
      console.error("Error generating resume:", error);
      if (error.response) {
        // The backend sends a JSON body explaining what went wrong. With
        // responseType 'blob' it arrives as a Blob, so read it back as text.
        let detail = "";
        try {
          const raw =
            error.response.data instanceof Blob
              ? await error.response.data.text()
              : error.response.data;
          const parsed = typeof raw === "string" ? JSON.parse(raw) : raw;
          detail = parsed?.message || parsed?.detail?.status || "";
        } catch {
          detail = "";
        }
        addTerminalMessage(
          detail
            ? `❌ ${detail}`
            : `❌ Server error: ${error.response.status} ${error.response.statusText}`,
          "error"
        );
      } else if (error.request) {
        // The request was made but no response was received
        addTerminalMessage(
          "❌ Network error: No response from server",
          "error"
        );
        addTerminalMessage(
          "Please check your connection and try again.",
          "error"
        );
      } else {
        // Something happened in setting up the request that triggered an Error
        addTerminalMessage(`❌ Request error: ${error.message}`, "error");
      }
    } finally {
      setIsGenerating(false);
      addTerminalMessage("Resume generation process completed.", "info");
    }
  };

  const toggleTips = () => {
    setShowTips(!showTips);
  };

  return (
    <div className="optimize-container">
      <NavBar />

      {/* Main Content */}
      <main className="optimize-main">
        <div className="optimize-content">
          {/* Main Row with Job Description and Sidebar */}
          <div className="optimize-main-row">
            {/* Left Section - Job Description */}
            <div className="optimize-left">
              <div className="job-input-section">
                {/* Title Row with Resume Name */}
                <div className="title-row">
                  <h2 className="section-title">Generate Resume</h2>
                  <div className="resume-name-input">
                    <Input
                      value={resumeName}
                      onChange={(e) => setResumeName(e.target.value)}
                      placeholder="Enter resume name"
                      className="resume-name-field"
                    />
                  </div>
                </div>

                {/* Subtitle Row with No Cache */}
                <div className="subtitle-row">
                  <p className="section-subtitle">
                    Paste the job description below to get your tailored resume
                  </p>
                  <div className="no-cache-switch">
                    <label className="switch-label">
                      <span className="switch-text">No Cache</span>
                      <div className="switch-container">
                        <input
                          type="checkbox"
                          checked={noCache}
                          onChange={(e) => setNoCache(e.target.checked)}
                          className="switch-input"
                        />
                        <span className="switch-slider"></span>
                      </div>
                    </label>
                  </div>
                </div>

                <div className="job-input-container">
                  <Textarea
                    value={jobDescription}
                    onChange={handleJobDescriptionChange}
                    placeholder="Paste the job description here..."
                    rows={12}
                    className="job-description-textarea"
                  />
                </div>
              </div>
            </div>
            {/* End of optimize-left */}

            {/* Right Sidebar */}
            <div className="optimize-sidebar">
              {/* Status Box */}
              <div className="status-box">
                <h3 className="status-box-title">Status Overview</h3>

                {/* Resume Status */}
                <div className="status-item">
                  <span className="status-item-label">Resume Status:</span>
                  <span className="status-placeholder">
                    {RESUME_STATUS_TEXT[userStatus?.resume_state] ||
                      "Not loaded yet"}
                  </span>
                </div>

                {/* Tweaking Status */}
                <div className="status-item">
                  <span className="status-item-label">Tweaking Status:</span>
                  <span className="status-placeholder">
                    {TWEAK_STATUS_TEXT[userStatus?.tweak_status] ||
                      "Not loaded yet"}
                  </span>
                </div>

                {/* Items in the master resume */}
                <div className="status-item">
                  <span className="status-item-label">Items:</span>
                  <span className="status-tokens">
                    {userStatus?.item_count ?? "—"}
                  </span>
                </div>
              </div>
              {/* End of status-box */}

              {/* Tips Widget */}
              <div className="tips-widget">
                <div className="tips-header" onClick={toggleTips}>
                  <h3 className="tips-title">Tips & Help</h3>
                  <span className={`tips-toggle ${showTips ? "expanded" : ""}`}>
                    {showTips ? "−" : "+"}
                  </span>
                </div>
                {showTips && (
                  <div className="tips-content">
                    <div className="tip-item">
                      <h4>📋 Job Description Tips</h4>
                      <ul>
                        <li>Copy the entire job posting for best results</li>
                        <li>
                          Include requirements, responsibilities, and preferred
                          qualifications
                        </li>
                        <li>Don't edit or summarize the original posting</li>
                      </ul>
                    </div>
                    <div className="tip-item">
                      <h4>⚡ Optimization Tips</h4>
                      <ul>
                        <li>Ensure your master resume is complete</li>
                        <li>Configure parameters for better matching</li>
                        <li>Review generated resume before submission</li>
                      </ul>
                    </div>
                    <div className="tip-item">
                      <h4>📞 Need Help?</h4>
                      <p>
                        Visit our help center or contact support for assistance
                        with resume optimization.
                      </p>
                    </div>
                  </div>
                )}
              </div>
              {/* End of tips-widget */}
            </div>
            {/* End of optimize-sidebar */}
          </div>
          {/* End of optimize-main-row */}

          {/* Terminal Output */}
          {showTerminal && (
            <div className="terminal-container">
              <div className="terminal-header">
                <span className="terminal-title">Resume Generation Log</span>
                <button
                  className="terminal-close"
                  onClick={() => setShowTerminal(false)}
                >
                  ×
                </button>
              </div>
              <div className="terminal-content">
                {terminalMessages.map((msg, index) => (
                  <div
                    key={index}
                    className={`terminal-line terminal-${msg.type}`}
                  >
                    <span className="terminal-timestamp">
                      [{msg.timestamp}]
                    </span>
                    <span className="terminal-message">{msg.message}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Generate Button - Full Width */}
          <Button
            variant="primary"
            onClick={handleGenerateResume}
            disabled={isGenerating || !jobDescription.trim()}
            className="generate-button"
          >
            {isGenerating ? "Generating Resume..." : "Generate Tailored Resume"}
          </Button>
        </div>
      </main>
    </div>
  );
};

export default Optimize;
