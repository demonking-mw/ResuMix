// src/context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import api from "../api/connection";

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
		const checkAuthState = async () => {
			try {
				const storedToken = localStorage.getItem("authToken");
				const storedReauthToken = localStorage.getItem("reauthToken");

				console.log("AuthContext - stored tokens on init:", {
					storedToken: !!storedToken,
					storedReauthToken: !!storedReauthToken,
				});

				if (storedToken && storedReauthToken) {
					// Decode the stored token to get user ID
					const decodedToken = jwtDecode(storedToken);
					const currentTime = Math.floor(Date.now() / 1000);

					// Check if token is still valid
					if (decodedToken.exp && currentTime < decodedToken.exp) {
						// Extract user ID from token
						const userId =
							decodedToken.sub || decodedToken.user_id || decodedToken.uid;

						if (userId) {
							// Attempt reauthentication with the backend
							try {
								console.log("AuthContext - attempting reauthentication...");
								const response = await api.get("/user", {
									params: {
										type: "re",
										uid: userId,
										reauth_jwt: storedReauthToken,
									},
								});

								console.log(
									"AuthContext - reauthentication response:",
									response.data
								);

								if (response.data.status) {
									// Update tokens if new ones are provided
									// The backend returns a new JWT that should be used as both auth and reauth token
									const newJwtToken = response.data.jwt;

									if (newJwtToken) {
										setToken(newJwtToken);
										setReauthToken(newJwtToken);
										localStorage.setItem("authToken", newJwtToken);
										localStorage.setItem("reauthToken", newJwtToken);
										console.log(
											"AuthContext - updated both tokens with new JWT"
										);
									} else {
										// If no new JWT provided, keep existing tokens
										setToken(storedToken);
										setReauthToken(storedReauthToken);
									}

									// Set user data from backend response
									const userDetails = response.data.detail;
									setUser({
										id: userDetails.uid,
										email: userDetails.email,
										name: userDetails.user_name || userDetails.uid,
										// Include any other user data from the backend
										...userDetails,
									});

									console.log(
										"AuthContext - reauthentication successful, user data updated"
									);
								} else {
									// Reauthentication failed, clear stored tokens and log out user
									console.log(
										"AuthContext - reauthentication failed, logging out user"
									);
									setUser(null);
									setToken(null);
									setReauthToken(null);
									localStorage.removeItem("authToken");
									localStorage.removeItem("reauthToken");
								}
							} catch (reauthError) {
								console.error(
									"AuthContext - reauthentication error:",
									reauthError
								);
								// If reauthentication fails due to network/server error, log out the user
								// This ensures we don't keep potentially invalid tokens
								console.log(
									"AuthContext - reauthentication failed due to error, logging out user"
								);
								setUser(null);
								setToken(null);
								setReauthToken(null);
								localStorage.removeItem("authToken");
								localStorage.removeItem("reauthToken");
							}
						} else {
							// No user ID in token, clear everything and log out
							console.log("AuthContext - no user ID in token, logging out");
							setUser(null);
							setToken(null);
							setReauthToken(null);
							localStorage.removeItem("authToken");
							localStorage.removeItem("reauthToken");
						}
					} else {
						// Token expired, clear it and log out
						console.log("AuthContext - token expired, logging out");
						setUser(null);
						setToken(null);
						setReauthToken(null);
						localStorage.removeItem("authToken");
						localStorage.removeItem("reauthToken");
					}
				}
			} catch (error) {
				console.error("Error checking auth state:", error);
				// Clear everything on any error during auth check
				setUser(null);
				setToken(null);
				setReauthToken(null);
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

	const reauthenticate = async () => {
		if (!reauthToken || !user?.id) {
			console.log(
				"AuthContext - no reauth token or user ID for reauthentication"
			);
			return false;
		}

		try {
			console.log("AuthContext - manual reauthentication attempt...");
			const response = await api.get("/user", {
				params: {
					type: "re",
					uid: user.id,
					reauth_jwt: reauthToken,
				},
			});

			if (response.data.status) {
				// Update tokens if new ones are provided
				// The backend returns a new JWT that should be used as both auth and reauth token
				const newJwtToken = response.data.jwt;

				if (newJwtToken) {
					setToken(newJwtToken);
					setReauthToken(newJwtToken);
					localStorage.setItem("authToken", newJwtToken);
					localStorage.setItem("reauthToken", newJwtToken);
					console.log(
						"AuthContext - manual reauth: updated both tokens with new JWT"
					);
				}

				// Update user data from backend response
				const userDetails = response.data.detail;
				setUser({
					id: userDetails.uid,
					email: userDetails.email,
					name: userDetails.user_name || userDetails.uid,
					// Include any other user data from the backend
					...userDetails,
				});

				console.log("AuthContext - manual reauthentication successful");
				return true;
			} else {
				console.log(
					"AuthContext - manual reauthentication failed, logging out"
				);
				// If manual reauthentication fails, log out the user
				setUser(null);
				setToken(null);
				setReauthToken(null);
				localStorage.removeItem("authToken");
				localStorage.removeItem("reauthToken");
				return false;
			}
		} catch (error) {
			console.error("AuthContext - manual reauthentication error:", error);
			// If manual reauthentication fails due to error, log out the user
			setUser(null);
			setToken(null);
			setReauthToken(null);
			localStorage.removeItem("authToken");
			localStorage.removeItem("reauthToken");
			return false;
		}
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
		reauthenticate,
	};

	return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
