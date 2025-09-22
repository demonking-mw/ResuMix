// src/components/Landing.jsx
import "./Landing.css";
import NavBar from "./NavBar";
import { useAuth } from "../context/AuthContext";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Landing() {
	const { isAuthenticated, logout } = useAuth();
	const navigate = useNavigate();

	useEffect(() => {
		if (isAuthenticated()) {
			logout();
		}
	}, [isAuthenticated()]);

	const handleBubbleClick = () => {
		navigate("/login");
	};

	return (
		<div className="landing-container">
			<NavBar />
			<main className="hero">
				<div className="hero-bubble" onClick={handleBubbleClick}>
					<h1 style={{ fontSize: '2.5rem' }}>
						Sentence-Transformer based Resume Optimizer
					</h1>
					<p>
						Set your resume once, then generate perfect, job-specific
						resumes in seconds.
					</p>
				</div>
			</main>
		</div>
	);
}
