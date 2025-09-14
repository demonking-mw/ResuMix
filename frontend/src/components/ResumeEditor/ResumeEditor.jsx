// src/components/ResumeEditor/ResumeEditor.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import api from "../../api/connection";
import "./ResumeEditor.css";
import SectionViewer from "./components/SectionViewer";
import ResumeHeader from "./components/ResumeHeader";
import ConfirmationModal from "./components/ConfirmationModal";
import HelpModal from "./components/HelpModal";
import { FormatHelpContent, ModeHelpContent } from "./components/HelpContent";
import { generateFullLatex } from "../../utils/generateFullLatex";
import { CopyToClipboard } from "react-copy-to-clipboard";
import { Highlight, themes } from "prism-react-renderer";
import { Clipboard, ClipboardCheck } from "lucide-react";

const ResumeEditor = ({
  mode = "view", // "view", "edit", "parameters-only", "view-latex"
  showParameters = true,
  showContent = true,
  onSave = null,
}) => {
  const { user, loading: authLoading, reauthToken } = useAuth();
  const navigate = useNavigate();
  const [resumeData, setResumeData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState("");
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [copyStatus, setCopyStatus] = useState(false);

  // Confirmation modal state
  const [confirmationModal, setConfirmationModal] = useState({
    isOpen: false,
    title: "",
    message: "",
    onConfirm: null,
    sectionIndex: null,
  });

  // Help modal state
  const [helpModal, setHelpModal] = useState({
    isOpen: false,
    type: null, // "format" or "mode"
  });

  // Add latex generation
  const getLatexContent = () => {
    if (!resumeData) return "";
    return generateFullLatex(resumeData);
  };

  // Create default resume structure for new accounts
  const createDefaultResumeData = () => {
    return {
      aux_info: { type: "resume" },
      heading_info: {
        heading_name: "Steve Smin",
        subsequent_content: ["steve@example.com"],
      },
      sections: [
        {
          sect_id: 0,
          aux_info: { type: "section" },
          title: "Sample Resume Section",
          items: [],
        },
      ],
    };
  };

  // Load resume data from user context (as shown in AccountHome.jsx line 18)
  useEffect(() => {
    console.log(
      "ResumeEditor useEffect - authLoading:",
      authLoading,
      "user:",
      user
    );
    console.log("User object keys:", user ? Object.keys(user) : "no user");
    console.log("user?.resumeinfo:", user?.resumeinfo);

    // Don't proceed if auth is still loading
    if (authLoading) {
      console.log("Auth still loading, waiting...");
      return;
    }

    try {
      // Check if user has valid resume data with required structure
      const hasValidResumeData =
        user?.resumeinfo &&
        user.resumeinfo.aux_info &&
        user.resumeinfo.heading_info &&
        user.resumeinfo.sections;

      if (hasValidResumeData) {
        console.log("Found valid resume data, loading...");
        setResumeData(user.resumeinfo);
        setIsLoading(false);
      } else {
        console.log(
          "No valid resume data found (empty object or missing structure). Creating default structure..."
        );
        console.log(
          "User resumeinfo:",
          JSON.stringify(user?.resumeinfo, null, 2)
        );
        // Create default resume structure for new accounts
        const defaultResume = createDefaultResumeData();
        console.log(
          "Created default resume:",
          JSON.stringify(defaultResume, null, 2)
        );
        setResumeData(defaultResume);
        setHasUnsavedChanges(true); // Mark as having changes since it's new
        setIsLoading(false);
      }
    } catch (err) {
      setError("Failed to load resume data");
      setIsLoading(false);
      console.error("Error loading resume data:", err);
    }
  }, [user, authLoading]);

  // Manual save function - triggered by save button
  const handleSaveResume = async () => {
    if (!resumeData || !user?.id || !reauthToken) {
      console.error("Missing required data:", {
        resumeData: !!resumeData,
        uid: !!user?.id,
        reauth_jwt: !!reauthToken,
      });
      setSaveMessage("❌ Missing user authentication data");
      return;
    }

    try {
      setIsSaving(true);
      setSaveMessage("Caching vectors...");

      // Prepare payload according to backend requirements
      const payload = {
        uid: user.id,
        reauth_jwt: reauthToken,
        resumeinfo: resumeData,
      };

      // Console log the resume data format before sending to backend
      console.log("=== RESUME DATA BEING SENT TO BACKEND ===");
      console.log("Full payload:", JSON.stringify(payload, null, 2));
      console.log(
        "Resume data structure:",
        JSON.stringify(resumeData, null, 2)
      );
      console.log("=== END RESUME DATA ===");

      const response = await api.post("/resume", payload);
      const data = response.data;

      if (data.status) {
        setSaveMessage("✅ Saved successfully");
        setHasUnsavedChanges(false); // Reset unsaved changes flag
        // Clear success message after 3 seconds
        setTimeout(() => setSaveMessage(""), 3000);
        return data;
      } else {
        const detail = data.detail?.status || data.message || "Unknown error";
        setSaveMessage(`❌ Save failed: ${detail}`);
        console.error("Save failed:", detail);
        throw new Error(detail);
      }
    } catch (err) {
      console.error("Resume save error:", err);
      // Check if it's an axios error with response
      if (err.response && err.response.data) {
        const detail =
          err.response.data.detail?.status ||
          err.response.data.message ||
          "Server error";
        setSaveMessage(`❌ Save failed: ${detail}`);
      } else {
        setSaveMessage("❌ Network error — please try again later.");
      }
      throw err;
    } finally {
      setIsSaving(false);
    }
  };

  // Resume update handler - no auto-save, just update state
  const handleResumeUpdate = (updatedData) => {
    console.log(
      "handleResumeUpdate called with:",
      JSON.stringify(updatedData, null, 2)
    );
    setResumeData(updatedData);
    setHasUnsavedChanges(true);
    // Call external onSave callback if provided
    if (onSave) {
      onSave(updatedData);
    }
  };

  // Deep clone helper for immutable updates
  const deepClone = (obj) => JSON.parse(JSON.stringify(obj));

  // Check if resume has meaningful content (not just default template)
  const isResumeEmpty = () => {
    if (!resumeData) return true;

    // Check if it's still the default template
    const isDefaultName =
      resumeData.heading_info?.heading_name === "Steve Smin";
    const hasEmptySections =
      !resumeData.sections ||
      resumeData.sections.length === 0 ||
      resumeData.sections.every(
        (section) => !section.items || section.items.length === 0
      );

    return isDefaultName && hasEmptySections;
  };

  // Update header handler
  const handleHeaderUpdate = (updatedHeader) => {
    console.log(
      "handleHeaderUpdate called with:",
      JSON.stringify(updatedHeader, null, 2)
    );
    console.log(
      "Current resumeData before header update:",
      JSON.stringify(resumeData, null, 2)
    );

    const updated = deepClone(resumeData);
    console.log("After deepClone:", JSON.stringify(updated, null, 2));

    // Ensure we have the full structure before updating
    if (!updated.aux_info) {
      console.log("ERROR: resumeData missing aux_info, recreating structure");
      const defaultResume = createDefaultResumeData();
      updated.aux_info = defaultResume.aux_info;
      updated.sections = defaultResume.sections;
    }

    updated.heading_info = updatedHeader;
    console.log("Final updated structure:", JSON.stringify(updated, null, 2));
    handleResumeUpdate(updated);
  };

  // Update section title
  const updateSectionTitle = (sectionIndex, newTitle) => {
    const updated = deepClone(resumeData);
    updated.sections[sectionIndex].title = newTitle;
    handleResumeUpdate(updated);
  };

  // Update item titles
  const updateItemTitles = (sectionIndex, itemIndex, titleIndex, newTitle) => {
    const updated = deepClone(resumeData);
    if (!updated.sections[sectionIndex].items[itemIndex].titles) {
      updated.sections[sectionIndex].items[itemIndex].titles = [];
    }
    updated.sections[sectionIndex].items[itemIndex].titles[titleIndex] =
      newTitle;
    handleResumeUpdate(updated);
  };

  // Add a new title field (with proper backend formatting)
  const addItemTitle = (sectionIndex, itemIndex) => {
    const updated = deepClone(resumeData);
    const item = updated.sections[sectionIndex].items[itemIndex];

    if (!item.titles) {
      item.titles = [];
    }

    // Add "title" string at the next position
    item.titles.push("");

    handleResumeUpdate(updated);
  };

  // Remove the last title field
  const removeLastItemTitle = (sectionIndex, itemIndex) => {
    const updated = deepClone(resumeData);
    const item = updated.sections[sectionIndex].items[itemIndex];

    if (item.titles && item.titles.length > 0) {
      // Remove the last title
      item.titles.pop();
    }

    handleResumeUpdate(updated);
  };

  // Helper function to strip HTML-like tags for content_str
  const stripMarkupTags = (text) => {
    if (!text) return "";
    // Remove HTML-like tags but preserve the text content
    return text.replace(/<[^>]*>/g, "");
  };

  // Update line content
  const updateLineContent = (
    sectionIndex,
    itemIndex,
    lineIndex,
    newContent
  ) => {
    const updated = deepClone(resumeData);
    // Store the raw content with markup for edit mode
    updated.sections[sectionIndex].items[itemIndex].lines[lineIndex].content =
      newContent;
    // Strip markup for clean display in view/parameters mode
    updated.sections[sectionIndex].items[itemIndex].lines[
      lineIndex
    ].content_str = stripMarkupTags(newContent);
    handleResumeUpdate(updated);
  };

  // Update item parameters
  const updateItemParameters = (sectionIndex, itemIndex, paramType, value) => {
    const updated = deepClone(resumeData);
    if (!updated.sections[sectionIndex].items[itemIndex].cate_scores) {
      updated.sections[sectionIndex].items[itemIndex].cate_scores = {
        weight: 1,
        bias: 0,
      };
    }
    updated.sections[sectionIndex].items[itemIndex].cate_scores[paramType] =
      value;
    handleResumeUpdate(updated);
  };

  // Add new section
  const addNewSection = () => {
    const updated = deepClone(resumeData);
    const newSection = {
      title: "NEW SECTION",
      sect_id: updated.sections.length,
      aux_info: { type: "section" },
      items: [],
    };
    updated.sections.push(newSection);
    handleResumeUpdate(updated);
  };

  // Delete section
  const deleteSection = (sectionIndex) => {
    const sectionTitle =
      resumeData?.sections?.[sectionIndex]?.title || "this section";

    setConfirmationModal({
      isOpen: true,
      title: "Delete Section",
      message: `Are you sure you want to delete "${sectionTitle}"? This action cannot be undone once you save. To undo this action, click cancel or reload the page.`,
      onConfirm: () => confirmDeleteSection(sectionIndex),
      sectionIndex: sectionIndex,
    });
  };

  // Actually delete the section after confirmation
  const confirmDeleteSection = (sectionIndex) => {
    const updated = deepClone(resumeData);
    updated.sections.splice(sectionIndex, 1);
    // Reindex section IDs
    updated.sections.forEach((section, index) => {
      section.sect_id = index;
    });
    handleResumeUpdate(updated);
    closeConfirmationModal();
  };

  // Close confirmation modal
  const closeConfirmationModal = () => {
    setConfirmationModal({
      isOpen: false,
      title: "",
      message: "",
      onConfirm: null,
      sectionIndex: null,
    });
  };

  // Open help modal
  const openHelpModal = (type) => {
    setHelpModal({
      isOpen: true,
      type: type,
    });
  };

  // Close help modal
  const closeHelpModal = () => {
    setHelpModal({
      isOpen: false,
      type: null,
    });
  };

  // Move section up
  const moveSectionUp = (sectionIndex) => {
    if (sectionIndex <= 0) return; // Can't move first section up
    const updated = deepClone(resumeData);
    // Swap sections
    const temp = updated.sections[sectionIndex];
    updated.sections[sectionIndex] = updated.sections[sectionIndex - 1];
    updated.sections[sectionIndex - 1] = temp;
    // Reindex section IDs
    updated.sections.forEach((section, index) => {
      section.sect_id = index;
    });
    handleResumeUpdate(updated);
  };

  // Move section down
  const moveSectionDown = (sectionIndex) => {
    if (sectionIndex >= resumeData.sections.length - 1) return; // Can't move last section down
    const updated = deepClone(resumeData);
    // Swap sections
    const temp = updated.sections[sectionIndex];
    updated.sections[sectionIndex] = updated.sections[sectionIndex + 1];
    updated.sections[sectionIndex + 1] = temp;
    // Reindex section IDs
    updated.sections.forEach((section, index) => {
      section.sect_id = index;
    });
    handleResumeUpdate(updated);
  };

  // Add new item to section
  const addNewItem = (sectionIndex) => {
    const updated = deepClone(resumeData);
    const newItem = {
      aux_info: { type: "items", style: "n" },
      titles: ["", "", ""],
      lines: [],
      cate_scores: { weight: 1.0, bias: 0.0 },
    };
    updated.sections[sectionIndex].items.push(newItem);
    handleResumeUpdate(updated);
  };

  // Add pre-populated item to section at specific position
  const addPrePopulatedItem = (sectionIndex, insertAfterIndex = -1) => {
    const updated = deepClone(resumeData);
    const newItem = {
      aux_info: { type: "items", style: "n" },
      titles: [""],
      lines: [
        {
          aux_info: { type: "lines" },
          content: "",
          content_str: "",
          cate_score: {
            technical: {},
            soft: {},
            relevance: {},
          },
          keywords: [],
        },
      ],
      cate_scores: { weight: 1.0, bias: 0.0 },
    };

    // Insert at specific position, at beginning, or at end
    if (insertAfterIndex === -1) {
      // Insert at the beginning
      updated.sections[sectionIndex].items.unshift(newItem);
    } else if (
      insertAfterIndex >= 0 &&
      insertAfterIndex < updated.sections[sectionIndex].items.length
    ) {
      // Insert after the specified index
      updated.sections[sectionIndex].items.splice(
        insertAfterIndex + 1,
        0,
        newItem
      );
    } else {
      // Insert at the end
      updated.sections[sectionIndex].items.push(newItem);
    }

    handleResumeUpdate(updated);
  };

  // Delete item from section
  const deleteItem = (sectionIndex, itemIndex) => {
    const updated = deepClone(resumeData);
    updated.sections[sectionIndex].items.splice(itemIndex, 1);
    handleResumeUpdate(updated);
  };

  // Add new line to item
  const addNewLine = (sectionIndex, itemIndex) => {
    const updated = deepClone(resumeData);
    const newLine = {
      aux_info: { type: "lines" },
      content: "",
      content_str: "",
      cate_score: {
        technical: {},
        soft: {},
        relevance: {},
      },
      keywords: [],
    };
    updated.sections[sectionIndex].items[itemIndex].lines.push(newLine);
    handleResumeUpdate(updated);
  };

  // Delete line from item
  const deleteLine = (sectionIndex, itemIndex, lineIndex) => {
    const updated = deepClone(resumeData);
    updated.sections[sectionIndex].items[itemIndex].lines.splice(lineIndex, 1);
    handleResumeUpdate(updated);
  };

  // Move item up within section
  const moveItemUp = (sectionIndex, itemIndex) => {
    if (itemIndex === 0) return; // Can't move first item up

    const updated = deepClone(resumeData);
    const items = updated.sections[sectionIndex].items;

    // Swap with previous item
    [items[itemIndex - 1], items[itemIndex]] = [
      items[itemIndex],
      items[itemIndex - 1],
    ];

    handleResumeUpdate(updated);
  };

  // Move item down within section
  const moveItemDown = (sectionIndex, itemIndex) => {
    const updated = deepClone(resumeData);
    const items = updated.sections[sectionIndex].items;

    if (itemIndex === items.length - 1) return; // Can't move last item down

    // Swap with next item
    [items[itemIndex], items[itemIndex + 1]] = [
      items[itemIndex + 1],
      items[itemIndex],
    ];

    handleResumeUpdate(updated);
  };

  // Loading state - show loading if auth is loading OR resume data is loading

  if (authLoading || isLoading) {
    return (
      <div className="resume-editor-container">
        <div className="resume-editor-loading">
          <div className="loading-spinner"></div>
          <p>
            Loading resume... (auth: {authLoading ? "loading" : "done"}, data:{" "}
            {isLoading ? "loading" : "done"})
          </p>
          <div className="loading-report-section">
            <p>Taking longer than expected?</p>
            <a
              href="https://forms.gle/xUyzrBY9MLnqSqkQ9"
              target="_blank"
              rel="noopener noreferrer"
              className="report-issue-button"
            >
              Report Issue
            </a>
          </div>
        </div>
      </div>
    );
  }

  // Error state - only show error if we couldn't create default data
  if (error && !resumeData) {
    return (
      <div className="resume-editor-container">
        <div className="resume-editor-error">
          <h3>Unable to Load Resume</h3>
          <p>{error}</p>
          <button
            className="retry-button"
            onClick={() => window.location.reload()}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  // Final safety check - if resumeData is still null, show loading
  if (!resumeData) {
    return (
      <div className="resume-editor-container">
        <div className="resume-editor-loading">
          <div className="loading-spinner"></div>
          <p>Preparing resume editor...</p>
        </div>
      </div>
    );
  }

  return mode === "view-latex" ? (
    <div className="latex-view">
      <div className="latex-content-wrapper">
        <Highlight
          theme={themes.vsLight}
          code={getLatexContent()}
          language="tex"
        >
          {({ className, style, tokens, getLineProps, getTokenProps }) => (
            <pre
              className={`${className} latex-content`}
              style={{
                ...style,
                padding: "1.5rem",
                borderRadius: "8px",
                margin: "1rem",
                fontSize: "14px",
                lineHeight: "1.5",
                position: "relative", // Added for absolute positioning of copy button
              }}
            >
              <div className="copy-button-wrapper">
                <CopyToClipboard
                  text={getLatexContent()}
                  onCopy={() => {
                    setCopyStatus("Copied!");
                    setTimeout(() => setCopyStatus(""), 1500);
                  }}
                >
                  <button className="copy-button">
                    {copyStatus ? (
                      <ClipboardCheck
                        className="clipboard-copy"
                        strokeWidth={1.75}
                      />
                    ) : (
                      <Clipboard
                        className="clipboard-copy"
                        strokeWidth={1.75}
                      />
                    )}{" "}
                    {copyStatus || "Copy code"}
                  </button>
                </CopyToClipboard>
              </div>
              {tokens.map((line, i) => (
                <div
                  key={i}
                  {...getLineProps({ line })}
                  style={{ display: "table-row" }}
                >
                  <span
                    style={{
                      display: "table-cell",
                      textAlign: "right",
                      paddingRight: "1rem",
                      userSelect: "none",
                      opacity: 0.5,
                      color: "#3b9d0eff",
                      width: "1%",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {i + 1}
                  </span>
                  <span style={{ display: "table-cell" }}>
                    {line.map((token, key) => (
                      <span key={key} {...getTokenProps({ token })} />
                    ))}
                  </span>
                </div>
              ))}
            </pre>
          )}
        </Highlight>
      </div>
    </div>
  ) : (
    <div className="resume-editor-container" data-mode={mode}>
      <div className="resume-editor-header">
        <div className="header-left">
          <h1>YOUR MASTER RESUME</h1>
        </div>
        <div className="header-right">
          {/* Format Help Button - always visible */}
          <button
            className="help-button"
            onClick={() => openHelpModal("format")}
          >
            <span className="help-button-icon">📝</span>
            Format Help
          </button>

          {/* Wiki Button - always visible */}
          <button className="help-button" onClick={() => navigate("/wiki")}>
            <span className="help-button-icon">📖</span>
            Wiki
          </button>

          {/* Mode Help Button - always visible */}
          <button className="help-button" onClick={() => openHelpModal("mode")}>
            <span className="help-button-icon">❓</span>
            Mode Guide
          </button>

          <div className="editor-mode-indicator">
            <span className={`mode-badge mode-${mode}`}>
              {mode === "view"
                ? "View Mode"
                : mode === "edit"
                ? "Edit Mode"
                : mode === "parameters-only"
                ? "Parameters Only"
                : "View LaTeX"}
            </span>
            {/* Save status indicator */}
            {(isSaving || saveMessage) && (
              <span
                className={`save-status ${
                  isSaving
                    ? "saving"
                    : saveMessage.includes("✅")
                    ? "success"
                    : "error"
                }`}
              >
                {saveMessage}
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="resume-editor-content">
        {/* Empty resume state for view mode */}
        {showContent && mode === "view" && isResumeEmpty() && (
          <div className="empty-resume-state">
            <div className="empty-resume-message">
              <h3>Your resume is empty</h3>
              <p>
                Get started by switching to the Edit tab to add your information
                and experience.
              </p>
              <div className="empty-resume-actions">
                <button
                  className="wiki-button"
                  onClick={() => window.open("", "_blank")}
                  disabled
                >
                  📖 View Resume Guide
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Resume Header Section */}
        {showContent && (!isResumeEmpty() || mode !== "view") && (
          <ResumeHeader
            headingInfo={resumeData.heading_info}
            mode={mode}
            onUpdate={handleHeaderUpdate}
          />
        )}

        {/* Resume Sections */}
        {showContent && (!isResumeEmpty() || mode !== "view") && (
          <div className="resume-sections">
            {resumeData.sections?.map((section, sectionIndex) => (
              <SectionViewer
                key={section.sect_id || sectionIndex}
                section={section}
                sectionIndex={sectionIndex}
                mode={mode}
                showParameters={showParameters}
                onUpdateSectionTitle={(newTitle) =>
                  updateSectionTitle(sectionIndex, newTitle)
                }
                onUpdateItemTitles={(itemIndex, titleIndex, newTitle) =>
                  updateItemTitles(
                    sectionIndex,
                    itemIndex,
                    titleIndex,
                    newTitle
                  )
                }
                onAddItemTitle={(itemIndex) =>
                  addItemTitle(sectionIndex, itemIndex)
                }
                onRemoveLastItemTitle={(itemIndex) =>
                  removeLastItemTitle(sectionIndex, itemIndex)
                }
                onUpdateLineContent={(itemIndex, lineIndex, newContent) =>
                  updateLineContent(
                    sectionIndex,
                    itemIndex,
                    lineIndex,
                    newContent
                  )
                }
                onUpdateItemParameters={(itemIndex, paramType, value) =>
                  updateItemParameters(
                    sectionIndex,
                    itemIndex,
                    paramType,
                    value
                  )
                }
                onAddNewItem={() => addNewItem(sectionIndex)}
                onAddPrePopulatedItem={(insertAfterIndex) =>
                  addPrePopulatedItem(sectionIndex, insertAfterIndex)
                }
                onDeleteItem={(itemIndex) =>
                  deleteItem(sectionIndex, itemIndex)
                }
                onAddNewLine={(itemIndex) =>
                  addNewLine(sectionIndex, itemIndex)
                }
                onDeleteLine={(itemIndex, lineIndex) =>
                  deleteLine(sectionIndex, itemIndex, lineIndex)
                }
                onMoveItemUp={(itemIndex) =>
                  moveItemUp(sectionIndex, itemIndex)
                }
                onMoveItemDown={(itemIndex) =>
                  moveItemDown(sectionIndex, itemIndex)
                }
                onDeleteSection={() => deleteSection(sectionIndex)}
                onMoveSectionUp={() => moveSectionUp(sectionIndex)}
                onMoveSectionDown={() => moveSectionDown(sectionIndex)}
                canMoveSectionUp={sectionIndex > 0}
                canMoveSectionDown={
                  sectionIndex < (resumeData.sections?.length || 0) - 1
                }
              />
            ))}
          </div>
        )}

        {/* Parameters-only view */}
        {mode === "parameters-only" && (
          <div className="parameters-only-view">
            <h2>Resume Parameters</h2>
            {resumeData.sections?.map((section, sectionIndex) => (
              <div
                key={section.sect_id || sectionIndex}
                className="section-viewer"
              >
                <div className="section-header">
                  <h3 className="section-title">{section.title}</h3>
                </div>
                <div className="section-items">
                  {section.items?.map((item, itemIndex) => {
                    // Determine what to display for the item
                    const getItemDisplayText = () => {
                      // Check if item has meaningful titles
                      const hasValidTitles =
                        item.titles &&
                        item.titles.some((title) => title && title.trim());

                      // If has valid titles, use them
                      if (hasValidTitles) {
                        return item.titles
                          .filter((title) => title && title.trim())
                          .join(" • ");
                      }

                      // If no valid titles but has exactly one line, use the line content
                      if (
                        item.lines &&
                        item.lines.length === 1 &&
                        item.lines[0].content_str
                      ) {
                        return item.lines[0].content_str;
                      }

                      // Fallback to "Untitled Item"
                      return "Untitled Item";
                    };

                    return (
                      <div key={itemIndex} className="item-viewer-compact">
                        <div className="item-text-section">
                          {getItemDisplayText()}
                        </div>
                        <div className="item-controls-section">
                          <div className="parameter-control-inline">
                            <div className="param-top-row">
                              <span className="param-label">weight:</span>
                              <span className="param-indicator">
                                {item.cate_scores?.weight > 1.2
                                  ? "🔥"
                                  : item.cate_scores?.weight > 1.0
                                  ? "⬆️"
                                  : item.cate_scores?.weight === 1.0
                                  ? "➡️"
                                  : item.cate_scores?.weight > 0.5
                                  ? "⬇️"
                                  : "❄️"}
                              </span>
                              <input
                                type="number"
                                value={item.cate_scores?.weight || 1}
                                step="0.01"
                                min="0"
                                max="2"
                                className="param-input-compact"
                                onChange={(e) =>
                                  updateItemParameters(
                                    sectionIndex,
                                    itemIndex,
                                    "weight",
                                    parseFloat(e.target.value) || 0
                                  )
                                }
                              />
                            </div>
                            <input
                              type="range"
                              value={item.cate_scores?.weight || 1}
                              step="0.01"
                              min="0"
                              max="2"
                              className="param-slider-compact"
                              onChange={(e) =>
                                updateItemParameters(
                                  sectionIndex,
                                  itemIndex,
                                  "weight",
                                  parseFloat(e.target.value)
                                )
                              }
                            />
                          </div>
                          <div className="parameter-control-inline">
                            <div className="param-top-row">
                              <span className="param-label">bias:</span>
                              <span className="param-indicator">
                                {item.cate_scores?.bias > 0.5
                                  ? "📈"
                                  : item.cate_scores?.bias > 0
                                  ? "📊"
                                  : item.cate_scores?.bias === 0
                                  ? "⚖️"
                                  : item.cate_scores?.bias > -0.5
                                  ? "📉"
                                  : "📉"}
                              </span>
                              <input
                                type="number"
                                value={item.cate_scores?.bias || 0}
                                step="0.01"
                                min="-2"
                                max="2"
                                className="param-input-compact"
                                onChange={(e) =>
                                  updateItemParameters(
                                    sectionIndex,
                                    itemIndex,
                                    "bias",
                                    parseFloat(e.target.value) || 0
                                  )
                                }
                              />
                            </div>
                            <input
                              type="range"
                              value={item.cate_scores?.bias || 0}
                              step="0.01"
                              min="-2"
                              max="2"
                              className="param-slider-compact"
                              onChange={(e) =>
                                updateItemParameters(
                                  sectionIndex,
                                  itemIndex,
                                  "bias",
                                  parseFloat(e.target.value)
                                )
                              }
                            />
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Manual save button for edit and parameters-only mode */}
      {(mode === "edit" || mode === "parameters-only") && (
        <div className="resume-editor-actions">
          <button
            className={`action-button save-button ${
              hasUnsavedChanges ? "has-changes" : "no-changes"
            }`}
            onClick={handleSaveResume}
            disabled={isSaving || !hasUnsavedChanges}
          >
            {isSaving
              ? "Saving..."
              : hasUnsavedChanges
              ? "Save Changes"
              : "No Changes"}
          </button>
        </div>
      )}

      {/* Add new section button for edit mode */}
      {mode === "edit" && (
        <div className="add-section-container">
          <button className="add-section-button" onClick={addNewSection}>
            + Add New Section
          </button>
        </div>
      )}

      {/* Confirmation Modal */}
      <ConfirmationModal
        isOpen={confirmationModal.isOpen}
        title={confirmationModal.title}
        message={confirmationModal.message}
        confirmText="Delete"
        cancelText="Cancel"
        onConfirm={confirmationModal.onConfirm}
        onCancel={closeConfirmationModal}
        isDangerous={true}
      />

      {/* Help Modal */}
      <HelpModal
        isOpen={helpModal.isOpen}
        title={
          helpModal.type === "format"
            ? "Text Formatting Guide"
            : helpModal.type === "mode"
            ? "Modes Guide"
            : ""
        }
        content={
          helpModal.type === "format" ? (
            <FormatHelpContent />
          ) : helpModal.type === "mode" ? (
            <ModeHelpContent />
          ) : null
        }
        onClose={closeHelpModal}
      />
    </div>
  );
};

export default ResumeEditor;
