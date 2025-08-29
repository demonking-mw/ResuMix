// src/wiki/Wiki.jsx
"use client";
import "./Wiki.css";
import NavBar from "../NavBar";
import { useState, useEffect } from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import { ChevronRight, BookOpen, Zap, Code, HelpCircle } from "lucide-react";

const wikiSections = [
	{
		id: "getting-started",
		title: "Getting Started",
		icon: <BookOpen className="w-4 h-4" />,
		content: {
			title: "Getting Started",
			description:
				"Learn the basics and get up and running quickly with our platform.",
			sections: [
				{
					heading: "Quick Start Guide",
					content:
						"Follow these steps to get started with your first project. This guide will walk you through the essential setup process and basic configuration.",
				},
				{
					heading: "Installation",
					content:
						"Install the necessary dependencies and configure your development environment. Make sure you have Node.js 18+ installed on your system.",
				},
				{
					heading: "First Steps",
					content:
						"Create your first project and understand the basic concepts. We'll cover project structure, configuration files, and basic usage patterns.",
				},
			],
		},
	},
	{
		id: "resume-optimization",
		title: "Resume Optimization",
		icon: <Zap className="w-4 h-4" />,
		content: {
			title: "Resume Optimization",
			description:
				"Advanced techniques and best practices for optimizing your resume content.",
			sections: [
				{
					heading: "Content Strategy",
					content:
						"Learn how to structure your resume content for maximum impact. Focus on achievements, quantifiable results, and relevant skills.",
				},
				{
					heading: "Keyword Optimization",
					content:
						"Understand how to incorporate industry-specific keywords and phrases that will help your resume pass through applicant tracking systems.",
				},
				{
					heading: "Format Guidelines",
					content:
						"Best practices for resume formatting, including layout, typography, and visual hierarchy to ensure readability and professional appearance.",
				},
			],
		},
	},
	{
		id: "api-usage",
		title: "API Usage",
		icon: <Code className="w-4 h-4" />,
		content: {
			title: "API Reference",
			description:
				"Complete API documentation with examples and integration guides.",
			sections: [
				{
					heading: "Authentication",
					content:
						"Learn how to authenticate your API requests using API keys or OAuth tokens. Include proper headers and handle authentication errors.",
				},
				{
					heading: "Endpoints",
					content:
						"Comprehensive list of available API endpoints, including request/response formats, parameters, and example calls for each endpoint.",
				},
				{
					heading: "Rate Limiting",
					content:
						"Understand API rate limits, how to handle rate limit responses, and best practices for efficient API usage in your applications.",
				},
			],
		},
	},
	{
		id: "troubleshooting",
		title: "Troubleshooting",
		icon: <HelpCircle className="w-4 h-4" />,
		content: {
			title: "Troubleshooting Guide",
			description:
				"Common issues and their solutions to help you resolve problems quickly.",
			sections: [
				{
					heading: "Common Issues",
					content:
						"Most frequently encountered problems and their step-by-step solutions. Check these first before reaching out for support.",
				},
				{
					heading: "Error Messages",
					content:
						"Detailed explanations of error messages you might encounter, what they mean, and how to resolve them effectively.",
				},
				{
					heading: "Getting Help",
					content:
						"When you need additional support, here's how to contact our team and what information to include in your support request.",
				},
			],
		},
	},
];


export default function Wiki() {
   const navigate = useNavigate();
   const location = useLocation();
   const { sectionId } = useParams();
   const currentSection = sectionId || "getting-started";
   const [activeSection, setActiveSection] = useState(currentSection);

   useEffect(() => {
	   setActiveSection(currentSection);
   }, [currentSection]);

	const handleSectionChange = (sectionId) => {
		setActiveSection(sectionId);
		navigate(`/wiki/${sectionId}`);
	};

	const currentSectionData =
		wikiSections.find((section) => section.id === activeSection) ||
		wikiSections[0];

	return (
		<div className="wiki-container">
			<NavBar />
			<div className="wiki-layout">
				<aside className="wiki-sidebar">
					<div className="wiki-sidebar-header">
						<h2 className="wiki-sidebar-title">Documentation</h2>
					</div>
					<nav className="wiki-sidebar-nav">
						{wikiSections.map((section) => (
							<button
								key={section.id}
								className={`wiki-sidebar-item ${
									activeSection === section.id ? "active" : ""
								}`}
								onClick={() => handleSectionChange(section.id)}
							>
								{section.icon}
								<span>{section.title}</span>
							</button>
						))}
					</nav>
				</aside>

				<main className="wiki-main">
					<div className="wiki-breadcrumb">
						<span className="wiki-breadcrumb-item">Documentation</span>
						<ChevronRight className="wiki-breadcrumb-separator" />
						<span className="wiki-breadcrumb-current">
							{currentSectionData.title}
						</span>
					</div>

					<div className="wiki-tabs-compact">
						{wikiSections.map((section) => (
							<button
								key={section.id}
								className={`wiki-tab-compact ${
									activeSection === section.id ? "active" : ""
								}`}
								onClick={() => handleSectionChange(section.id)}
							>
								{section.icon}
								<span className="wiki-tab-text">{section.title}</span>
							</button>
						))}
					</div>

					<div className="wiki-content-modern">
						<header className="wiki-content-header">
							<h1 className="wiki-content-title">
								{currentSectionData.content.title}
							</h1>
							<p className="wiki-content-description">
								{currentSectionData.content.description}
							</p>
						</header>

						<div className="wiki-content-body">
							{currentSectionData.content.sections.map((section, index) => (
								<section key={index} className="wiki-content-section">
									<h2 className="wiki-section-heading">{section.heading}</h2>
									<p className="wiki-section-content">{section.content}</p>
								</section>
							))}
						</div>
					</div>
				</main>
			</div>
		</div>
	);
}
