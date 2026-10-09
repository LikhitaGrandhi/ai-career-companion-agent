import React, { useState } from "react";
import "./Auth.css";

function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState("");
  const passwordRules = {
  length: formData.password.length >= 8,
  uppercase: /[A-Z]/.test(formData.password),
  lowercase: /[a-z]/.test(formData.password),
  number: /[0-9]/.test(formData.password),
  special: /[^A-Za-z0-9]/.test(formData.password),
};

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

    setErrors({
      ...errors,
      [e.target.name]: "",
    });

    setMessage("");
  };

  const validate = () => {
    const newErrors = {};

    if (!isLogin && !formData.name.trim()) {
      newErrors.name = "Name is required";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Enter a valid email address";
    }

   if (!formData.password) {
  newErrors.password = "Password is required";
} else if (
  !passwordRules.length ||
  !passwordRules.uppercase ||
  !passwordRules.lowercase ||
  !passwordRules.number ||
  !passwordRules.special
) {
  newErrors.password = "Password does not meet all requirements";
}

    if (!isLogin) {
      if (!formData.confirmPassword) {
        newErrors.confirmPassword = "Please confirm your password";
      } else if (formData.password !== formData.confirmPassword) {
        newErrors.confirmPassword = "Passwords do not match";
      }
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

const handleSubmit = async (e) => {
  e.preventDefault();

  if (!validate()) {
    return;
  }

  if (isLogin) {
  try {
    setMessage("Logging in...");

    const response = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: formData.email,
        password: formData.password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      setMessage(data.detail || "Invalid email or password.");
      return;
    }

    setMessage(`Welcome, ${data.name}!`);
    setTimeout(() => {
  localStorage.setItem("user_id", data.user_id);
  localStorage.setItem("user_name", data.name);

  if (data.student_id) {
    localStorage.setItem("student_id", data.student_id);
  } else {
    localStorage.removeItem("student_id");
  }

  localStorage.removeItem("generated_resume_id");
  localStorage.removeItem("generated_cover_letter_id");

  onLogin();
}, 700);
  } catch (error) {
    console.error("Login error:", error);
    setMessage("Unable to connect to the server.");
  }

  return;
}

  try {
    setMessage("Creating your account...");

    const response = await fetch("http://127.0.0.1:8000/auth/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      setMessage(data.detail || "Registration failed.");
      return;
    }

    setMessage("Account created successfully! You can now log in.");

    setTimeout(() => {
      setIsLogin(true);

      setFormData({
        name: "",
        email: formData.email,
        password: "",
        confirmPassword: "",
      });

      setErrors({});
      setMessage("");
    }, 1200);

  } catch (error) {
    console.error("Signup error:", error);
    setMessage("Unable to connect to the server.");
  }
};

  return (
    <div className="auth-page">

      {/* Left Section */}
      <div className="auth-left">

        <div className="auth-brand">
          <span>🚀</span>
          <strong>AI Career Companion</strong>
        </div>

        <div className="auth-intro">
          <p className="auth-badge">
            ✨ AI-Powered Career Platform
          </p>

          <h1>
            Build your career
            <span> smarter with AI.</span>
          </h1>

          <p>
            Discover internships, analyze your skill gaps,
            improve your resume, prepare for interviews and
            manage your applications from one platform.
          </p>
        </div>

        <div className="auth-features">
          <div>
            <span>🎯</span>
            <p>Personalized internship matching</p>
          </div>

          <div>
            <span>📊</span>
            <p>AI-powered skill gap analysis</p>
          </div>

          <div>
            <span>🎤</span>
            <p>Interview preparation</p>
          </div>
        </div>

      </div>

      {/* Right Section */}
      <div className="auth-right">

        <div className="auth-card">

          <div className="auth-card-header">

            <h2>
              {isLogin ? "Welcome Back 👋" : "Create Your Account"}
            </h2>

            <p>
              {isLogin
                ? "Login to continue your career journey."
                : "Start your personalized career journey with AI."}
            </p>

          </div>

          <form onSubmit={handleSubmit}>

            {!isLogin && (
              <div className="form-group">
                <label>Full Name</label>

                <input
                  type="text"
                  name="name"
                  placeholder="Enter your full name"
                  value={formData.name}
                  onChange={handleChange}
                />

                {errors.name && (
                  <small className="error">
                    {errors.name}
                  </small>
                )}
              </div>
            )}

            <div className="form-group">
              <label>Email Address</label>

              <input
                type="email"
                name="email"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
              />

              {errors.email && (
                <small className="error">
                  {errors.email}
                </small>
              )}
            </div>

            <div className="form-group">
              <label>Password</label>

              <input
                type="password"
                name="password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
              />
              {!isLogin && (
  <div className="password-rules">

    <div className={passwordRules.length ? "rule valid" : "rule"}>
      {passwordRules.length ? "✓" : "○"} At least 8 characters
    </div>

    <div className={passwordRules.uppercase ? "rule valid" : "rule"}>
      {passwordRules.uppercase ? "✓" : "○"} One uppercase letter
    </div>

    <div className={passwordRules.lowercase ? "rule valid" : "rule"}>
      {passwordRules.lowercase ? "✓" : "○"} One lowercase letter
    </div>

    <div className={passwordRules.number ? "rule valid" : "rule"}>
      {passwordRules.number ? "✓" : "○"} One number
    </div>

    <div className={passwordRules.special ? "rule valid" : "rule"}>
      {passwordRules.special ? "✓" : "○"} One special character
    </div>

  </div>
)}

              {errors.password && (
                <small className="error">
                  {errors.password}
                </small>
              )}
            </div>

            {!isLogin && (
              <div className="form-group">
                <label>Confirm Password</label>

                <input
                  type="password"
                  name="confirmPassword"
                  placeholder="Re-enter your password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                />

                {errors.confirmPassword && (
                  <small className="error">
                    {errors.confirmPassword}
                  </small>
                )}
              </div>
            )}

            {message && (
              <div className="auth-message">
                {message}
              </div>
            )}

            <button
              type="submit"
              className="auth-submit"
            >
              {isLogin ? "Login →" : "Create Account →"}
            </button>

          </form>

          <div className="auth-switch">

            {isLogin ? (
              <>
                Don't have an account?
                <button
                  type="button"
                  onClick={() => {
                    setIsLogin(false);
                    setErrors({});
                    setMessage("");
                  }}
                >
                  Sign Up
                </button>
              </>
            ) : (
              <>
                Already have an account?
                <button
                  type="button"
                  onClick={() => {
                    setIsLogin(true);
                    setErrors({});
                    setMessage("");
                  }}
                >
                  Login
                </button>
              </>
            )}

          </div>

        </div>

      </div>

    </div>
  );
}

export default Auth;