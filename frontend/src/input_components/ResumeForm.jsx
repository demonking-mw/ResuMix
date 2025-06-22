import { useState } from "react";
import SectionForm from "./SectionForm";
import "./ResumeForm.css";
import { Link } from "react-router-dom";
import logo from "../assets/ResuMix.png";

export default function ResumeForm() {
  const [headingName, setHeadingName] = useState("");
  const [subsequentContent, setSubsequentContent] = useState([]);
  const [subsequentContentRaw, setSubsequentContentRaw] = useState("");
  const [sections, setSections] = useState([]);
  const [jobDescription, setJobDescription] = useState("");

  const addSection = () => {
    setSections([...sections, { title: "", items: [] }]);
  };

  const updateSection = (index, updatedSection) => {
    const updated = [...sections];
    updated[index] = updatedSection;
    setSections(updated);
  };

  const deleteSection = (index) => {
    const updated = sections.filter((_, i) => i !== index);
    setSections(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const resumeDict = {
      aux_info: { type: "resume" },
      heading_info: {
        heading_name: headingName,
        subsequent_content: subsequentContent,
      },
      sections: sections.map((section, i) => ({
        sect_id: i,
        aux_info: { type: "section" },
        title: section.title,
        items: section.items.map((item) => ({
          aux_info: { type: "items", style: "n" },
          titles: item.titles.filter((title) => title.trim() !== ""),
          lines: item.lines.map((line) => ({
            aux_info: { type: "lines" },
            content: line.content_str,
            content_str: line.content_str,
            cate_score: {
              technical: {},
              soft: {},
              relevance: {},
            },
            keywords: [],
          })),
          cate_scores: {
            technical: { weight: 1.0, bias: 1.0 },
            soft: { weight: 1.0, bias: 1.0 },
            relevance: { weight: 1.0, bias: 1.0 },
          },
        })),
      })),
    };
    const payload = {
      resume_dict: resumeDict,
      job_description: jobDescription,
    };

    try {
      const response = await fetch("http://localhost:5001/api/generate-resume", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("Resume generation failed");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "resume.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error(err);
      alert("Failed to generate resume");
    }
  };

  return (
    <div className="layout">
      <header style={{ position: "absolute", top: "1rem", left: "1.5rem" }}>
        <Link to="/" className="logo-link" style={{ display: "flex", alignItems: "center", textDecoration: "none" }}>
          <img src={logo} alt="ResuMix Logo" className="home-logo" />
          <span className="brand-name">ResuMix</span>
        </Link>
      </header>

      <p className="text-style">My Mix</p>

      <div className="form-bg">
        <form className="form-style" onSubmit={handleSubmit}>
          <input
            placeholder="Your Name"
            value={headingName}
            onChange={(e) => setHeadingName(e.target.value)}
            required
          />
          <textarea
            placeholder={`Enter one item per line (e.g. Links, Email, Phone...)`}
            value={subsequentContentRaw}
            onChange={(e) => {
              const raw = e.target.value;
              setSubsequentContentRaw(raw);
              const lines = raw.split("\n").map((line) => line.trim()).filter((line) => line !== "");
              setSubsequentContent(lines);
            }}
            rows={Math.max(subsequentContent.length, 3)}
          />
          <textarea
            placeholder="Paste job description here"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            style={{ minHeight: "120px" }}
            required
          />

          {sections.map((section, idx) => (
            <SectionForm
              key={idx}
              index={idx}
              data={section}
              updateSection={(updated) => updateSection(idx, updated)}
              deleteSection={() => deleteSection(idx)}
            />
          ))}
          <button type="button" onClick={addSection}>Add Section</button>
          <button className="resume-button" type="submit">Generate Resume</button>
        </form>
      </div>
    </div>
  );
}
