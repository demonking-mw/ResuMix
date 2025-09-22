// src/wiki/Wiki.jsx
"use client";
import "./Wiki.css";
import NavBar from "../NavBar";
import { useState, useEffect } from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import { ChevronRight, BookOpen, Zap, Code, HelpCircle } from "lucide-react";

const wikiSections = [
  {
    id: "the-basics",
    title: "The basics",
    icon: <BookOpen className="w-4 h-4" />,
    content: {
      title: "About ResuMix: must-know basics",
      description:
        "How the app function, what data it uses, and key features to get you started.",
      sections: [
        {
          heading: "General Overview",
          content:
            "ResuMix is a resume-optimizer that helps you create tailored resumes for job applications. It uses Sentence Transformers to analyze job descriptions and optimize your resume content accordingly. Your resume content is NOT thrown into any LLM, so your data remains private and secure.",
        },
        {
          heading: "Optimization behind the hood",
          content:
            "Each time you generate a resume, ResuMix parses the job description with AI, then feeds the output into a sentence transformer model to measure semantic similarity between your resume content and the job description. This scores each line of your resume, which is later used to make the best scoring resume. The resume is automatically downloaded as a PDF. Depending on server load, this process would take around 5-30 seconds. We hope to upgrade our compute soon to make this faster, but budget is a great limiting factor.",
        },
        {
          heading: "LaTeX Master Resume",
          content:
            "Under 'Set Your Master Resume', you can find a section which provides you with a LaTeX version of your resume. This LaTeX code represents your master resume, which is the base format used for generating tailored resumes. You can copy and paste this LaTeX code into your own LaTeX editor or Overleaf to make further customizations or adjustments to the layout and design of your resume.",
        },
        { heading: "Data Structure",
          content:
            "Your resume data is structured in a nested format with sections, items, and lines. Each section contains multiple items, and each item contains multiple lines. This structure allows for detailed organization of your resume content, making it easier to manage and optimize.",
        },
        
      ],
    },
  },
  {
    id: "resume-operations",
    title: "Resume Operations",
    icon: <Zap className="w-4 h-4" />,
    content: {
      title: "Resume Operations",
      description:
        "Step-by-step guide on inputting, tuning, and optimizing your resume.",
      sections: [
        {
          heading: "Inputting Your Resume: basics",
          content:
            "Select the edit mode in the resume page (if it's not already selected). Add a section and give it a title. Now you can add items to the section. Worry less about the order of the items, as you can reorder them later. When adding items, set the number of titles you want to see. They would automatically goes into a certain format. You should use the same number of titles for a section. To achieve the bullet point effect commonly seen in SKILLS sections, remove every single titles, and you will see a different input style for lines.",
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
