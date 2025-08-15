// Example usage of the UI Library
import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  Button,
  Input,
  Textarea,
  Card,
  Title,
  Navbar,
  Hero,
  PageWrapper,
  AuthWrapper,
  FormWrapper,
  Divider,
  LoadingSpinner,
  ErrorMessage,
  Container,
} from "../ui";
import logo from "../assets/ResuMix.png";

const UILibraryDemo = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
      alert("Form submitted!");
    }, 2000);
  };

  return (
    <PageWrapper>
      {/* Navigation Example */}
      <Navbar logo={logo} brandText="ResuMix" logoLink="/">
        <Button variant="outline" size="sm" as={Link} to="/login">
          Login
        </Button>
        <Button variant="landing" as={Link} to="/signup">
          Sign Up
        </Button>
      </Navbar>

      {/* Hero Section Example */}
      <Hero>
        <Title variant="hero" as="h1">
          UI Library Demo
        </Title>
        <p className="subtitle">
          This demonstrates all the reusable components created from your
          existing designs.
        </p>
      </Hero>

      {/* Form Example */}
      <FormWrapper>
        <Card variant="form">
          <Title variant="section">Contact Form</Title>

          <form onSubmit={handleSubmit} className="flex flex-col gap-lg">
            <Input
              label="Full Name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter your name"
              required
            />

            <Input
              label="Email Address"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter your email"
              required
            />

            <Textarea
              label="Message"
              name="message"
              value={formData.message}
              onChange={handleChange}
              placeholder="Your message here..."
              rows={5}
              required
            />

            <ErrorMessage>{error}</ErrorMessage>

            <Button type="submit" disabled={loading} className="w-full">
              {loading ? <LoadingSpinner size="sm" /> : "Send Message"}
            </Button>
          </form>

          <Divider />

          <div className="text-center">
            <p className="text-muted">
              Or reach out via email:{" "}
              <a href="mailto:hello@resumix.com" className="text-blue">
                hello@resumix.com
              </a>
            </p>
          </div>
        </Card>
      </FormWrapper>

      {/* Button Examples */}
      <Container>
        <div
          className="p-3xl bg-white"
          style={{ margin: "2rem auto", borderRadius: "12px" }}
        >
          <Title variant="section">
            Button Examples (Your Existing Designs)
          </Title>

          <div className="flex gap-lg flex-wrap">
            <Button variant="primary" width="auto">
              Primary Button
            </Button>
            <Button variant="landing">Landing Button</Button>
            <Button variant="form">Form Button</Button>
            <Button variant="resume">Resume Button</Button>
          </div>

          <div className="flex gap-lg flex-wrap" style={{ marginTop: "1rem" }}>
            <Button variant="primary" size="sm" width="auto">
              Small Primary
            </Button>
            <Button variant="form">Base Form</Button>
            <Button variant="resume" size="lg">
              Large Resume
            </Button>
          </div>

          <div className="flex gap-lg flex-wrap" style={{ marginTop: "1rem" }}>
            <Button variant="primary" disabled width="auto">
              Disabled Primary
            </Button>
            <Button variant="landing" disabled>
              Disabled Landing
            </Button>
          </div>
        </div>
      </Container>

      {/* Card Examples */}
      <Container>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
            gap: "1rem",
            margin: "2rem auto",
          }}
        >
          <Card>
            <div className="card-header">
              <Title variant="section" className="text-lg">
                Default Card
              </Title>
            </div>
            <div className="card-body">
              <p>This is a standard card with header and body sections.</p>
            </div>
          </Card>

          <Card variant="auth">
            <Title variant="section">Auth Card</Title>
            <p>This card is styled for authentication forms.</p>
            <Button variant="primary" className="w-full">
              Login
            </Button>
          </Card>
        </div>
      </Container>
    </PageWrapper>
  );
};

export default UILibraryDemo;
