import "./NavBar.css";
import { Link, useNavigate } from "react-router-dom";
import logo from "../assets/ResuMix.png";
import { useAuth } from "../context/AuthContext";

export default function NavBar() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <div className="navbar">
      <Link
        to={`${isAuthenticated() ? "/account" : "/"}`}
        className="logo-link"
      >
        <img src={logo} alt="ResuMix Logo" className="logo" />
        <span className="brand-name">ResuMix</span>
      </Link>
      {isAuthenticated() ? (
        <div className="user-actions">
          <span className="welcome-text">
            Welcome, {user?.name || user?.user_name || user?.id || "User"}!
          </span>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      ) : (
        <div className="nav-actions">
          <Link to="/login">
            <p className="landing-button">Log in</p>
          </Link>
          <Link to="/signup">
            <p className="landing-button">Sign up ↗</p>
          </Link>
        </div>
      )}
    </div>
  );
}
