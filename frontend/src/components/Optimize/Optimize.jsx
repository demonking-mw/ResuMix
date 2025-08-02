// src/components/Optimize/Optimize.jsx
import React, { useState, useEffect, useRef } from "react";
import { useAuth } from "../../context/AuthContext";
import "./Optimize.css";
import NavBar from "../NavBar";
import { Button, Textarea } from "../../ui";

const Optimize = () => {
	const { user, getReauthHeaders } = useAuth();
	const [jobDescription, setJobDescription] = useState("");
	const [isGenerating, setIsGenerating] = useState(false);
	const [showTips, setShowTips] = useState(false);
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

	const handleJobDescriptionChange = (e) => {
		setJobDescription(e.target.value);
	};

	const handleGenerateResume = async () => {
		if (!jobDescription.trim()) {
			alert("Please enter a job description before generating your resume.");
			return;
		}

		setIsGenerating(true);

		try {
			// Reauthenticate before making the API call
			const reauthSuccess = await reauthenticate();
			if (!reauthSuccess) {
				alert("Authentication failed. Please log in again.");
				setIsGenerating(false);
				return;
			}

			// TODO: Replace with actual API endpoint for resume generation
			const response = await fetch("/api/generate-resume", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					...getReauthHeaders(),
				},
				body: JSON.stringify({
					job_description: jobDescription,
				}),
			});

			if (response.ok) {
				// Handle successful resume generation
				const blob = await response.blob();
				const url = window.URL.createObjectURL(blob);
				const a = document.createElement("a");
				a.style.display = "none";
				a.href = url;
				a.download = "tailored_resume.pdf";
				document.body.appendChild(a);
				a.click();
				window.URL.revokeObjectURL(url);
				document.body.removeChild(a);
			} else {
				throw new Error("Failed to generate resume");
			}
		} catch (error) {
			console.error("Error generating resume:", error);
			alert("There was an error generating your resume. Please try again.");
		} finally {
			setIsGenerating(false);
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
								<h2 className="section-title">Job Description</h2>
								<p className="section-subtitle">
									Paste the job description below to get your tailored resume
								</p>
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
										Will be implemented later
									</span>
								</div>

								{/* Tweaking Status */}
								<div className="status-item">
									<span className="status-item-label">Tweaking Status:</span>
									<span className="status-placeholder">
										Will be implemented later
									</span>
								</div>

								{/* Tokens (Future Implementation) */}
								<div className="status-item">
									<span className="status-item-label">Tokens:</span>
									<span className="status-tokens">
										(implemented in the future)
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
