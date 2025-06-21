import { useState } from "react";
import ItemForm from "./ItemForm";
import { Trash2 } from "lucide-react";
import "./SectionForm.css";
import "./Trash.css";

export default function SectionForm({
  index,
  data,
  updateSection,
  deleteSection,
}) {
  const [numTitles, setNumTitles] = useState(2);

  const updateTitle = (e) => {
    updateSection({ ...data, title: e.target.value });
  };

  const handleNumTitlesChange = (e) => {
    setNumTitles(parseInt(e.target.value));
  };

  const addItem = () => {
    const titlesArray = Array(numTitles).fill("");
    updateSection({
      ...data,
      items: [...data.items, { titles: titlesArray, lines: [] }],
    });
  };

  const updateItem = (itemIndex, newItem) => {
    const updatedItems = [...data.items];
    updatedItems[itemIndex] = newItem;
    updateSection({ ...data, items: updatedItems });
  };

  const deleteItem = (itemIndex) => {
    const updatedItems = data.items.filter((_, i) => i !== itemIndex);
    updateSection({ ...data, items: updatedItems });
  };

  return (
    <div className="section-form">
      <div className="group-trash">
        <input
          placeholder="Section Title"
          value={data.title}
          onChange={updateTitle}
        />
        <Trash2 className="trash-button" onClick={deleteSection} />
      </div>

      <label style={{ marginLeft: "1rem" }}># of Titles:</label>
      <select value={numTitles} onChange={handleNumTitlesChange}>
        {[0, 2, 3, 4, 5].map((n) => (
          <option key={n} value={n}>
            {n}
          </option>
        ))}
      </select>

      {data.items.map((item, i) => (
        <ItemForm
          key={i}
          index={i}
          data={item}
          updateItem={(newItem) => updateItem(i, newItem)}
          numTitles={numTitles}
          deleteItem={() => deleteItem(i)}
        />
      ))}
      <button type="button" onClick={addItem}>
        Add Item
      </button>
    </div>
  );
}
