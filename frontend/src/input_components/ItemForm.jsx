import LineForm from "./LineForm";
import "./ItemForm.css";
import "./Trash.css";
import { Trash2 } from "lucide-react";

export default function ItemForm({
  index,
  data,
  updateItem,
  numTitles,
  deleteItem,
}) {
  const updateTitle = (titleIndex, value) => {
    const updated = [...data.titles];
    updated[titleIndex] = value;
    updateItem({ ...data, titles: updated });
  };

  const addLine = () => {
    updateItem({ ...data, lines: [...data.lines, { content_str: "" }] });
  };

  const updateLine = (lineIndex, newLine) => {
    const updatedLines = [...data.lines];
    updatedLines[lineIndex] = newLine;
    updateItem({ ...data, lines: updatedLines });
  };

  const deleteLine = (lineIndex) => {
    const updatedLines = data.lines.filter((_, i) => i !== lineIndex);
    updateItem({ ...data, lines: updatedLines });
  };

  const titleFormats = {
    0: [],
    2: ["Role", "Dates"],
    3: ["Role", "Augmentation", "Dates"],
    4: ["Role", "Date", "Company", "Location"],
    5: ["Role", "Augmentation", "Dates", "Company", "Location"],
  };

  const labels = titleFormats[numTitles] || [];

  return (
    <div className="item-form">
      {labels.map((label, i) => (
        <input
          key={i}
          placeholder={label}
          value={data.titles[i] || ""}
          onChange={(e) => updateTitle(i, e.target.value)}
        />
      ))}

      <div
        className="group-trash"
        style={{ justifyContent: "justify-between !important" }}
      >
        <button type="button" onClick={addLine}>
          Add Line
        </button>
        <Trash2 className="trash-button" onClick={deleteItem} />
      </div>

      {data.lines.map((line, idx) => (
        <LineForm
          key={idx}
          index={idx}
          data={line}
          updateLine={(newLine) => updateLine(idx, newLine)}
          deleteLine={() => deleteLine(idx)}
        />
      ))}
    </div>
  );
}
