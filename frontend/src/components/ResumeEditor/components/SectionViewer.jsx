// src/components/ResumeEditor/components/SectionViewer.jsx
import React from "react";
import ItemViewer from "./ItemViewer";

const SectionViewer = ({
  section,
  sectionIndex,
  mode,
  showParameters,
  onUpdateSectionTitle,
  onUpdateItemTitles,
  onAddItemTitle,
  onRemoveLastItemTitle,
  onUpdateLineContent,
  onUpdateItemParameters,
  onAddNewItem,
  onAddPrePopulatedItem,
  onDeleteItem,
  onAddNewLine,
  onDeleteLine,
  onMoveItemUp,
  onMoveItemDown,
  onDeleteSection,
  onMoveSectionUp,
  onMoveSectionDown,
  canMoveSectionUp,
  canMoveSectionDown,
}) => {
  if (!section) {
    return (
      <div className="section-viewer">
        <div className="section-placeholder">
          <p>Section data not available</p>
        </div>
      </div>
    );
  }

  // Detect if this section is primarily compact items (like Skills)
  const compactItemsCount =
    section.items?.filter((item) => {
      const hasNoTitles =
        !item.titles ||
        item.titles.length === 0 ||
        item.titles.every((title) => !title || title.trim() === "");
      const hasSingleLine = item.lines && item.lines.length === 1;
      return hasNoTitles && hasSingleLine;
    }).length || 0;

  const totalItems = section.items?.length || 0;
  const isCompactSection =
    totalItems > 0 && compactItemsCount / totalItems > 0.7; // 70% or more are compact

  return (
    <div
      className={`section-viewer ${
        isCompactSection ? "compact-section" : "standard-section"
      }`}
    >
      {/* Section Header */}
      <div className="section-header">
        <div className="section-title-container">
          {mode === "edit" ? (
            <input
              type="text"
              value={section.title || ""}
              className="section-title-input"
              placeholder="Section Title"
              onChange={(e) => onUpdateSectionTitle(e.target.value)}
            />
          ) : (
            <h2 className="section-title">
              {section.title || "Untitled Section"}
            </h2>
          )}
        </div>

        {/* Section metadata - visible in debug/dev mode */}
        <div className="section-metadata">
          <span className="section-id">ID: {section.sect_id}</span>
          <span className="section-stats">
            {totalItems} items ({compactItemsCount} compact)
          </span>
        </div>

        {/* Section controls for edit mode */}
        {mode === "edit" && (
          <div className="section-controls">
            <button
              className="move-up-button"
              onClick={onMoveSectionUp}
              disabled={!canMoveSectionUp}
              title="Move section up"
            >
              ↑
            </button>
            <button
              className="move-down-button"
              onClick={onMoveSectionDown}
              disabled={!canMoveSectionDown}
              title="Move section down"
            >
              ↓
            </button>
            <button
              className="edit-button delete-button"
              onClick={onDeleteSection}
              title="Delete this section"
            >
              Delete Section
            </button>
          </div>
        )}
      </div>

      {/* Section Items */}
      <div className="section-items">
        {section.items?.length > 0 ? (
          <>
            {/* Add item button before first item (only in edit mode) */}
            {mode === "edit" && (
              <div className="add-item-between">
                <button
                  className="add-item-between-button"
                  onClick={() => onAddPrePopulatedItem(-1)}
                  title="Add new pre-filled item at beginning"
                >
                  Add Item
                </button>
              </div>
            )}
            {section.items.map((item, itemIndex) => (
              <React.Fragment key={itemIndex}>
                <ItemViewer
                  item={item}
                  itemIndex={itemIndex}
                  sectionIndex={sectionIndex}
                  mode={mode}
                  showParameters={showParameters}
                  onUpdateTitles={(titleIndex, newTitle) =>
                    onUpdateItemTitles(itemIndex, titleIndex, newTitle)
                  }
                  onAddTitle={() => onAddItemTitle(itemIndex)}
                  onRemoveLastTitle={() => onRemoveLastItemTitle(itemIndex)}
                  onUpdateLineContent={(lineIndex, newContent) =>
                    onUpdateLineContent(itemIndex, lineIndex, newContent)
                  }
                  onUpdateParameters={(paramType, value) =>
                    onUpdateItemParameters(itemIndex, paramType, value)
                  }
                  onAddNewLine={() => onAddNewLine(itemIndex)}
                  onDeleteLine={(lineIndex) =>
                    onDeleteLine(itemIndex, lineIndex)
                  }
                  onMoveUp={() => onMoveItemUp(itemIndex)}
                  onMoveDown={() => onMoveItemDown(itemIndex)}
                  onDeleteItem={() => onDeleteItem(itemIndex)}
                  canMoveUp={itemIndex > 0}
                  canMoveDown={itemIndex < (section.items?.length || 0) - 1}
                />
                {/* Small add item button between items (only in edit mode) */}
                {mode === "edit" && (
                  <div className="add-item-between">
                    <button
                      className="add-item-between-button"
                      onClick={() => onAddPrePopulatedItem(itemIndex)}
                      title="Add new pre-filled item"
                    >
                      Add Item
                    </button>
                  </div>
                )}
              </React.Fragment>
            ))}
          </>
        ) : (
          <div className="empty-section">
            <p className="empty-message">No items in this section</p>
            {mode === "edit" && (
              <div className="add-item-between">
                <button
                  className="add-item-between-button"
                  onClick={() => onAddPrePopulatedItem(-1)}
                  title="Add new pre-filled item"
                >
                  Add Item
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SectionViewer;
