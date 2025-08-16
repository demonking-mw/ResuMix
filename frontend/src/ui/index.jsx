// UI Components Library
import React from "react";
import "../ui/base.css";
import "../ui/components.css";

// Button Component - Using exact existing designs
export const Button = ({
  children,
  variant = "primary",
  width = null,
  className = "",
  disabled = false,
  onClick,
  type = "button",
  as = "button",
  ...props
}) => {
  const variantClass = `btn-${variant}`;
  const widthClass = width ? `btn-${width}` : "";

  const classes = [variantClass, widthClass, className]
    .filter(Boolean)
    .join(" ");

  const Component = as;

  return (
    <Component
      className={classes}
      disabled={disabled}
      onClick={onClick}
      type={type}
      {...props}
    >
      {children}
    </Component>
  );
};

// Input Component
export const Input = ({
  label,
  error,
  className = "",
  type = "text",
  placeholder,
  value,
  onChange,
  required = false,
  ...props
}) => {
  const inputClass = `form-input ${className}`;

  return (
    <div className="form-group">
      {label && (
        <label className="form-label">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}
      <input
        className={inputClass}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required={required}
        {...props}
      />
      {error && <div className="form-error">{error}</div>}
    </div>
  );
};

// Textarea Component
export const Textarea = ({
  label,
  error,
  className = "",
  placeholder,
  value,
  onChange,
  required = false,
  rows = 4,
  ...props
}) => {
  const textareaClass = `form-textarea ${className}`;

  return (
    <div className="form-group">
      {label && (
        <label className="form-label">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}
      <textarea
        className={textareaClass}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required={required}
        rows={rows}
        {...props}
      />
      {error && <div className="form-error">{error}</div>}
    </div>
  );
};

// Card Component
export const Card = ({
  children,
  variant = "default",
  className = "",
  ...props
}) => {
  const baseClass = "card";
  const variantClass = variant !== "default" ? `card-${variant}` : "";

  const classes = [baseClass, variantClass, className]
    .filter(Boolean)
    .join(" ");

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

// Title Component
export const Title = ({
  children,
  variant = "section",
  className = "",
  as = "h2",
  ...props
}) => {
  const baseClass = "title";
  const variantClass = `title-${variant}`;

  const classes = [baseClass, variantClass, className]
    .filter(Boolean)
    .join(" ");

  const Component = as;

  return (
    <Component className={classes} {...props}>
      {children}
    </Component>
  );
};

// Navbar Component
export const Navbar = ({
  logo,
  brandText,
  logoLink = "/",
  children,
  className = "",
  ...props
}) => {
  return (
    <nav className={`navbar ${className}`} {...props}>
      <a href={logoLink} className="nav-brand">
        {logo && <img src={logo} alt="Logo" className="nav-logo" />}
        {brandText && <span className="nav-brand-text">{brandText}</span>}
      </a>
      <div className="nav-actions">{children}</div>
    </nav>
  );
};

// Hero Section Component
export const Hero = ({ children, className = "", bubble = true, ...props }) => {
  return (
    <main className={`hero ${className}`} {...props}>
      {bubble ? <div className="hero-bubble">{children}</div> : children}
    </main>
  );
};

// Page Wrapper Component
export const PageWrapper = ({ children, className = "", ...props }) => {
  return (
    <div className={`page-wrapper ${className}`} {...props}>
      {children}
    </div>
  );
};

// Auth Wrapper Component
export const AuthWrapper = ({ children, className = "", ...props }) => {
  return (
    <div className={`auth-wrapper ${className}`} {...props}>
      {children}
    </div>
  );
};

// Form Wrapper Component
export const FormWrapper = ({ children, className = "", ...props }) => {
  return (
    <div className={`form-wrapper ${className}`} {...props}>
      {children}
    </div>
  );
};

// Divider Component
export const Divider = ({ className = "", ...props }) => {
  return <hr className={`divider ${className}`} {...props} />;
};

// Loading Spinner Component
export const LoadingSpinner = ({ size = "md", className = "" }) => {
  const sizeClasses = {
    sm: "w-4 h-4",
    md: "w-8 h-8",
    lg: "w-12 h-12",
  };

  return (
    <div className={`flex justify-center items-center ${className}`}>
      <div
        className={`animate-spin rounded-full border-2 border-gray-300 border-t-blue-600 ${sizeClasses[size]}`}
        style={{
          animation: "spin 1s linear infinite",
        }}
      />
    </div>
  );
};

// Error Message Component
export const ErrorMessage = ({ children, className = "" }) => {
  if (!children) return null;

  return <div className={`form-error ${className}`}>{children}</div>;
};

// Container Component
export const Container = ({ children, className = "", ...props }) => {
  return (
    <div className={`container ${className}`} {...props}>
      {children}
    </div>
  );
};
