import "./LineForm.css";
import "./Trash.css";
import { Trash2 } from "lucide-react";
export default function LineForm({ data, updateLine, deleteLine }) {
  return (
    <div className="line-form">
      <div className="group-trash">
        <textarea
          className="line-input"
          placeholder="Bullet Point"
          value={data.content_str}
          onChange={(e) => updateLine({ ...data, content_str: e.target.value })}
          rows={1}
        />
        <Trash2 className="trash-button" onClick={deleteLine} />
      </div>
    </div>
  );
}
