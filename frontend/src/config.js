// Runtime configuration for the local-first frontend.
// Values come from Vite env vars (frontend/.env); the defaults target a
// backend running on this machine, so no configuration is needed to start.

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5001";

// Google sign-in is optional: without a client id the button is hidden and
// email/password login is used instead.
export const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || "";

export const GOOGLE_LOGIN_ENABLED = Boolean(GOOGLE_CLIENT_ID);
