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
        "Learn how to create and customize your first resume with ResuMix.",
      sections: [
        {
          heading: "Create Your Resume",
          content:
            "Start by entering your name and contact information in the header section. Then use the 'Add Section' button to create sections like Education, Experience, Skills etc. Add items within each section to list your experiences and achievements.",
        },
        {
          heading: "Job Description Optimization",
          content:
            "Paste the job description you're applying for. ResuMix will analyze it and help tailor your resume content to highlight the most relevant skills and experiences for that specific role.",
        },
        {
          heading: "Preview & Download",
          content:
            "Once you've added your content, click 'Generate Resume' to create your customized PDF resume. You can preview it and make further edits before downloading.",
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
            "Best practices for resume formatting, including layout, typography, and visual hierarchy to ensure readability and professional appearance. Future support for copy and paste LaTeX code aligning with the optimized layout",
        },
        {
          heading: "Content Parameters",
          content:
            "Use the Parameters Mode to adjust weights and bias for each item. Higher weight means the item is more likely to be included in tailored resumes. Bias affects how the item is scored against job requirements.",
        },
        {
          heading: "Category Scoring",
          content:
            "ResuMix categorizes your experiences into Technical Skills, Soft Skills, and Job Relevance. Each line is scored based on these categories to help optimize content selection for specific jobs.",
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
            "All API requests require authentication. The system uses JWT tokens for session management. Include credentials in requests to protected endpoints.",
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
        {
          heading: "Data Structure",
          content:
            "Resume data uses a nested structure with sections, items and lines. Each level includes aux_info for type identification and additional metadata for optimization.",
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
      description: "Common issues and solutions when using ResuMix.",
      sections: [
        {
          heading: "Resume Generation Issues",
          content:
            "If resume generation fails, check that all required fields are filled. Make sure section titles and items follow the expected format.",
        },
        {
          heading: "Authentication Errors",
          content:
            "For login issues, ensure your credentials are correct. The system allows OAuth for authentication. Try clearing your browser cache or re-authenticating if session errors occur.",
        },
        {
          heading: "Content Optimization",
          content:
            "If content optimization seems incorrect, review the parameters in Parameters Mode. Adjust weights and bias values to fine-tune how items are selected. Ensure job descriptions contain relevant keywords for better matching.",
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
