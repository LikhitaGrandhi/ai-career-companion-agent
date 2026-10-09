import React from "react";
import "./Landing.css";

function Landing({ onGetStarted }) {
  return (
    <div className="landing-page">

      {/* Navigation */}
      <nav className="landing-nav">
        <div className="landing-logo">
          <span>🚀</span>
          <h2>AI Career Companion</h2>
        </div>

        <div className="landing-nav-actions">
  <button
    className="landing-login-link"
    onClick={onGetStarted}
  >
    Login
  </button>

  <button
    className="landing-login-btn"
    onClick={onGetStarted}
  >
    Sign Up
  </button>
</div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">

        <div className="hero-content">
          <p className="hero-badge">
            ✨ AI-Powered Career Assistant
          </p>

          <h1>
            Your Personal
            <span> AI Career Companion</span>
          </h1>

          <p className="hero-description">
            Discover the right internships, identify your skill gaps,
            improve your resume, prepare for interviews, and manage
            your applications — all in one place.
          </p>

          <div className="hero-buttons">
            <button
              className="primary-btn"
              onClick={onGetStarted}
            >
              Get Started →
            </button>

            <button
              className="secondary-btn"
              onClick={() =>
                document
                  .getElementById("features")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              Explore Features
            </button>
          </div>
        </div>

        <div className="hero-visual">
          <div className="career-card">
            <div className="career-card-header">
              <span>Career Dashboard</span>
              <span>●</span>
            </div>

            <div className="match-card">
              <div>
                <small>Internship Match</small>
                <h2>85%</h2>
              </div>
              <span className="match-icon">🎯</span>
            </div>

            <div className="skill-card">
              <div className="skill-header">
                <span>Python</span>
                <span>90%</span>
              </div>
              <div className="progress">
                <div style={{ width: "90%" }}></div>
              </div>

              <div className="skill-header">
                <span>Machine Learning</span>
                <span>82%</span>
              </div>
              <div className="progress">
                <div style={{ width: "82%" }}></div>
              </div>

              <div className="skill-header">
                <span>React</span>
                <span>68%</span>
              </div>
              <div className="progress">
                <div style={{ width: "68%" }}></div>
              </div>
            </div>
          </div>
        </div>

      </section>

      {/* Features */}
      <section id="features" className="features-section">

        <div className="section-heading">
          <p>Everything you need</p>
          <h2>Build Your Career With AI</h2>
          <span>
            From finding opportunities to preparing for interviews,
            your entire career journey in one platform.
          </span>
        </div>

        <div className="features-grid">

          <div className="feature-card">
            <div className="feature-icon">🔎</div>
            <h3>Internship Matching</h3>
            <p>
              Find internships that match your skills and career goals
              using AI-powered job matching.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Skill Gap Analysis</h3>
            <p>
              Identify the skills you are missing and understand what
              you need to learn for your target roles.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📄</div>
            <h3>Resume & Cover Letter</h3>
            <p>
              Generate personalized career documents based on the
              internship you are targeting.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🎤</div>
            <h3>Interview Preparation</h3>
            <p>
              Practice technical, project, role-specific and behavioral
              interview questions.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">💬</div>
            <h3>AI Career Assistant</h3>
            <p>
              Get personalized career guidance and recommendations
              whenever you need them.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">📋</div>
            <h3>Application Tracker</h3>
            <p>
              Track applications, deadlines, interview schedules and
              application progress in one place.
            </p>
          </div>

        </div>

      </section>

      {/* Bottom CTA */}
      <section className="cta-section">
        <h2>Ready to accelerate your career?</h2>
        <p>
          Let AI help you discover opportunities and prepare for your
          next internship.
        </p>

        <button
          className="primary-btn"
          onClick={onGetStarted}
        >
          Start Your Career Journey →
        </button>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div>
          <strong>🚀 AI Career Companion</strong>
          <p>AI-powered internship and career assistance.</p>
        </div>

        <p>© 2026 AI Career Companion</p>
      </footer>

    </div>
  );
}

export default Landing;