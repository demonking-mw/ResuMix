// src/components/Landing.jsx
import "./Landing.css";
import NavBar from "./NavBar";
import { useAuth } from "../context/AuthContext";
import { useEffect } from "react";

export default function Landing() {
  const { isAuthenticated, logout } = useAuth();

  useEffect(() => {
    if (isAuthenticated()) {
      logout();
    }
  }, [isAuthenticated()]);

  return (
    <div className="landing-container">
      <NavBar />
      <main className="hero">
        <div className="hero-bubble">
          <h1>
            Optimize Your Resume.
            <br />
            Maximize Your Impact.
          </h1>
          <p>
            Upload your resume once, then generate the perfect, job-specific
            resume in seconds.
          </p>
        </div>
      </main>
    </div>
  );
}
