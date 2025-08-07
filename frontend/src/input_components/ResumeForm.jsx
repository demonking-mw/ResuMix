import { useState } from "react";
import SectionForm from "./SectionForm";
import "./ResumeForm.css";
import { useAuth } from "../context/AuthContext";
import NavBar from "../components/NavBar";
import api from "../api/connection";

export default function ResumeForm() {
	const [headingName, setHeadingName] = useState("");
	const [subsequentContent, setSubsequentContent] = useState([]);
	const [subsequentContentRaw, setSubsequentContentRaw] = useState("");
	const [sections, setSections] = useState([]);
	const [jobDescription, setJobDescription] = useState("");
	const { isAuthenticated, user } = useAuth();

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
						weight: 1.0,
						bias: 1.0,
					},
				})),
			})),
		};
		const payload = {
			resume_dict: resumeDict,
			job_description: jobDescription,
		};

		try {
			const response = await api.post("/api/generate-resume", payload, {
				responseType: "blob",
			});

			// Axios response is automatically parsed, response.data contains the blob
			const blob = response.data;
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

	if (!isAuthenticated()) {
		return <Navigate to="/" replace />;
	}

	return (
		<div className="layout">
			<NavBar />

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
							const lines = raw
								.split("\n")
								.map((line) => line.trim())
								.filter((line) => line !== "");
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
					<button type="button" onClick={addSection}>
						Add Section
					</button>
					<button className="resume-button" type="submit">
						Generate Resume
					</button>
				</form>
			</div>
		</div>
	);
}
