// src/components/ExampleReauthUsage.jsx
import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useReauth } from "../hooks/useReauth";

export default function ExampleReauthUsage() {
	const { user, isAuthenticated } = useAuth();
	const { makeReauthRequest } = useReauth();
	const [userInfo, setUserInfo] = useState(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");

	const fetchUserInfo = async () => {
		if (!isAuthenticated()) {
			setError("You must be logged in to use this feature");
			return;
		}

		setLoading(true);
		setError("");

		try {
			// Example of using reauth to get user info
			const response = await makeReauthRequest("/user", {}, "GET");

			if (response.data.status) {
				setUserInfo(response.data.detail);
			} else {
				setError("Failed to fetch user info");
			}
		} catch (err) {
			console.error("Error fetching user info:", err);
			setError(
				"Failed to fetch user info: " + (err.message || "Network error")
			);
		} finally {
			setLoading(false);
		}
	};

	if (!isAuthenticated()) {
		return (
			<div className="example-reauth">
				<h3>Reauth Example</h3>
				<p>Please log in to see this example in action.</p>
			</div>
		);
	}

	return (
		<div className="example-reauth">
			<h3>Reauth Example</h3>
			<p>Current user: {user?.name || user?.email}</p>

			<button
				onClick={fetchUserInfo}
				disabled={loading}
				style={{
					padding: "10px 20px",
					backgroundColor: "#007bff",
					color: "white",
					border: "none",
					borderRadius: "4px",
					cursor: loading ? "not-allowed" : "pointer",
					marginBottom: "20px",
				}}
			>
				{loading ? "Loading..." : "Fetch User Info (Reauth)"}
			</button>

			{error && (
				<div style={{ color: "red", marginBottom: "10px" }}>Error: {error}</div>
			)}

			{userInfo && (
				<div
					style={{
						background: "#f8f9fa",
						padding: "15px",
						borderRadius: "4px",
						border: "1px solid #dee2e6",
					}}
				>
					<h4>User Information (from reauth):</h4>
					<pre>{JSON.stringify(userInfo, null, 2)}</pre>
				</div>
			)}
		</div>
	);
}
