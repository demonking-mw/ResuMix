// src/context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext({});

export const useAuth = () => {
	const context = useContext(AuthContext);
	if (!context) {
		throw new Error("useAuth must be used within an AuthProvider");
	}
	return context;
};

export const AuthProvider = ({ children }) => {
	const [user, setUser] = useState(null);
	const [loading, setLoading] = useState(true);
	const [token, setToken] = useState(null);
	const [reauthToken, setReauthToken] = useState(null);

	// Check if user is logged in on app start
	useEffect(() => {
		const checkAuthState = () => {
			try {
				const storedToken = localStorage.getItem("authToken");
				const storedReauthToken = localStorage.getItem("reauthToken");

				console.log("AuthContext - stored tokens on init:", {
					storedToken: !!storedToken,
					storedReauthToken: !!storedReauthToken,
				});

				if (storedToken) {
					// Decode and validate the token
					const decodedToken = jwtDecode(storedToken);
					const currentTime = Math.floor(Date.now() / 1000);

					// Check if token is still valid
					if (decodedToken.exp && currentTime < decodedToken.exp) {
						setToken(storedToken);
						setReauthToken(storedReauthToken);
						console.log(
							"AuthContext - setting reauthToken to:",
							storedReauthToken
						);
						setUser({
							id: decodedToken.sub || decodedToken.user_id,
							email: decodedToken.email,
							name: decodedToken.name || decodedToken.given_name,
							picture: decodedToken.picture,
							// Add other user data from your JWT as needed
						});
					} else {
						// Token expired, clear it
						localStorage.removeItem("authToken");
						localStorage.removeItem("reauthToken");
					}
				}
			} catch (error) {
				console.error("Error checking auth state:", error);
				localStorage.removeItem("authToken");
				localStorage.removeItem("reauthToken");
			} finally {
				setLoading(false);
			}
		};

		checkAuthState();
	}, []);

	const login = (token, userData = null, reauthJwt = null) => {
		try {
			console.log("AuthContext login called with:", {
				token: !!token,
				userData: !!userData,
				reauthJwt: !!reauthJwt,
			});

			setToken(token);
			localStorage.setItem("authToken", token);

			// Store the reauth JWT token if provided
			if (reauthJwt) {
				console.log("AuthContext - storing reauthJwt:", reauthJwt);
				setReauthToken(reauthJwt);
				localStorage.setItem("reauthToken", reauthJwt);
			} else {
				console.log("AuthContext - no reauthJwt provided");
			}

			if (userData) {
				setUser(userData);
			} else {
				// Decode user data from token if not provided
				const decodedToken = jwtDecode(token);
				setUser({
					id: decodedToken.sub || decodedToken.user_id,
					email: decodedToken.email,
					name: decodedToken.name || decodedToken.given_name,
					picture: decodedToken.picture,
				});
			}
		} catch (error) {
			console.error("Error during login:", error);
			throw error;
		}
	};

	const logout = () => {
		setUser(null);
		setToken(null);
		setReauthToken(null);
		localStorage.removeItem("authToken");
		localStorage.removeItem("reauthToken");
	};

	const isAuthenticated = () => {
		return !!user && !!token;
	};

	const getAuthHeaders = () => {
		return token ? { Authorization: `Bearer ${token}` } : {};
	};

	const getReauthHeaders = () => {
		return reauthToken && user?.id
			? {
					uid: user.id,
					reauth_jwt: reauthToken,
			  }
			: {};
	};

	const value = {
		user,
		token,
		reauthToken,
		loading,
		login,
		logout,
		isAuthenticated,
		getAuthHeaders,
		getReauthHeaders,
	};

	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
