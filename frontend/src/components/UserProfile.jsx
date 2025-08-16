// src/components/UserProfile.jsx
import React from "react";
import { useAuth } from "../context/AuthContext";

const UserProfile = () => {
  const { user, logout } = useAuth();

  if (!user) {
    return <div>No user data available</div>;
  }

  return (
    <div
      style={{
        padding: "20px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        margin: "10px",
      }}
    >
      <h3>User Profile</h3>
      <div style={{ display: "flex", alignItems: "center", gap: "15px" }}>
        {user.picture && (
          <img
            src={user.picture}
            alt="Profile"
            style={{ width: "50px", height: "50px", borderRadius: "50%" }}
          />
        )}
        <div>
          <p>
            <strong>Name:</strong> {user.name || "N/A"}
          </p>
          <p>
            <strong>Email:</strong> {user.email || "N/A"}
          </p>
          <p>
            <strong>ID:</strong> {user.id || "N/A"}
          </p>
        </div>
      </div>
      <button
        onClick={logout}
        style={{
          marginTop: "10px",
          padding: "8px 16px",
          backgroundColor: "#ff4444",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Logout
      </button>
    </div>
  );
};

export default UserProfile;
