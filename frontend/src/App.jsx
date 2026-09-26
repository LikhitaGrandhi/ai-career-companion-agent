import React, { useEffect, useState } from "react";

import "./App.css";



const API_URL = "http://127.0.0.1:8000";



function App() {

  const [activePage, setActivePage] = useState("Dashboard");



  // =========================================================

  // RESUME STATES

  // =========================================================

  const [selectedFile, setSelectedFile] = useState(null);

  const [uploading, setUploading] = useState(false);

  const [resumeData, setResumeData] = useState(null);

  const [uploadMessage, setUploadMessage] = useState("");



  // =========================================================

  // STUDENT ID

  // =========================================================

  const [studentId, setStudentId] = useState(

    localStorage.getItem("student_id") || ""

  );



  // =========================================================

  // INTERNSHIP STATES

  // =========================================================

  const [internshipMatches, setInternshipMatches] = useState([]);

  const [internshipLoading, setInternshipLoading] = useState(false);

  const [internshipError, setInternshipError] = useState("");

  const [customizedResume, setCustomizedResume] = useState(null);

  const [coverLetter, setCoverLetter] = useState("");

  const [careerActionLoading, setCareerActionLoading] = useState("");

  const [careerActionError, setCareerActionError] = useState("");

  const [careerActionJobId, setCareerActionJobId] = useState("");

// =========================================================
// INTERVIEW PREP STATES
// =========================================================

const [interviewPlan, setInterviewPlan] = useState(null);
const [interviewJobId, setInterviewJobId] = useState("");
const [interviewLoading, setInterviewLoading] = useState(false);
const [interviewError, setInterviewError] = useState("");

// =========================================================
// AI CAREER ASSISTANT STATES
// =========================================================

const [careerQuestion, setCareerQuestion] = useState("");
const [careerResponse, setCareerResponse] = useState("");
const [careerIntent, setCareerIntent] = useState("");
const [careerLoading, setCareerLoading] = useState(false);
const [careerError, setCareerError] = useState("");

  // =========================================================

  // SKILL GAP STATES

  // =========================================================

  const [skillGapResults, setSkillGapResults] = useState([]);

  const [skillGapLoading, setSkillGapLoading] = useState(false);

  const [skillGapError, setSkillGapError] = useState("");



  // =========================================================

  // MENU

  // =========================================================

  const menuItems = [

    { name: "Dashboard", icon: "⌂" },

    { name: "My Profile", icon: "👤" },

    { name: "Resume", icon: "📄" },

    { name: "Internships", icon: "💼" },

    { name: "Skill Gap", icon: "🎯" },

    { name: "Interview Prep", icon: "🎤" },

    { name: "AI Assistant", icon: "✨" },

  ];



  // =========================================================

  // DEMO DASHBOARD INTERNSHIPS

  // =========================================================

  const demoInternships = [

    {

      company: "Google",

      role: "Software Engineering Intern",

      location: "Bangalore",

      match: "92%",

    },

    {

      company: "Microsoft",

      role: "Software Engineer Intern",

      location: "Hyderabad",

      match: "88%",

    },

    {

      company: "Amazon",

      role: "SDE Intern",

      location: "Chennai",

      match: "84%",

    },

  ];



  // =========================================================

  // RESUME UPLOAD

  // =========================================================

  const handleResumeUpload = async () => {

    if (!selectedFile) {

      setUploadMessage("Please select a PDF resume first.");

      return;

    }



    if (selectedFile.type !== "application/pdf") {

      setUploadMessage("Only PDF files are allowed.");

      return;

    }



    setUploading(true);

    setUploadMessage("");

    setResumeData(null);



    const formData = new FormData();

    formData.append("file", selectedFile);



    try {

      const response = await fetch(`${API_URL}/resume/upload`, {

        method: "POST",

        body: formData,

      });



      const data = await response.json();



      if (!response.ok) {

        throw new Error(data.detail || "Resume upload failed.");

      }



      setResumeData(data.extracted_data);



      if (data.student_id) {

        setStudentId(data.student_id);



        localStorage.setItem(

          "student_id",

          data.student_id

        );

      }



      setUploadMessage(

        "Resume uploaded and analyzed successfully! 🎉"

      );

    } catch (error) {

      console.error("Upload error:", error);



      setUploadMessage(

        "Unable to upload resume. Make sure the FastAPI backend is running."

      );

    } finally {

      setUploading(false);

    }

  };



  // =========================================================

  // FILE SELECTION

  // =========================================================

  const handleFileChange = (event) => {

    const file = event.target.files[0];



    if (!file) {

      setSelectedFile(null);

      return;

    }



    setSelectedFile(file);

    setUploadMessage("");

    setResumeData(null);

  };



  // =========================================================

  // GET STUDENT ID

  // =========================================================

  const loadStudentId = async () => {

    if (studentId) {

      return studentId;

    }



    try {

      const response = await fetch(`${API_URL}/students`);



      if (!response.ok) {

        throw new Error("Unable to fetch students.");

      }



      const students = await response.json();



      if (!students || students.length === 0) {

        throw new Error(

          "No student profile found. Please upload your resume first."

        );

      }



      const latestStudent =

        students[students.length - 1];



      if (!latestStudent._id) {

        throw new Error("Student ID not found.");

      }



      setStudentId(latestStudent._id);



      localStorage.setItem(

        "student_id",

        latestStudent._id

      );



      return latestStudent._id;

    } catch (error) {

      console.error(

        "Student loading error:",

        error

      );



      throw error;

    }

  };



  // =========================================================

  // LOAD INTERNSHIP MATCHES

  // =========================================================

  const loadInternshipMatches = async () => {

    setInternshipLoading(true);

    setInternshipError("");



    try {

      const id = await loadStudentId();



      const response = await fetch(

        `${API_URL}/internships/${id}`

      );



      const data = await response.json();



      if (!response.ok) {

        throw new Error(

          data.detail ||

            "Unable to load internship matches."

        );

      }



      setInternshipMatches(

        data.matches || []

      );

    } catch (error) {

      console.error(

        "Internship loading error:",

        error

      );



      setInternshipError(

        error.message ||

          "Unable to load internship matches."

      );



      setInternshipMatches([]);

    } finally {

      setInternshipLoading(false);

    }

  };



  // =========================================================

  // LOAD SKILL GAP ANALYSIS

  // =========================================================

  const loadSkillGap = async () => {

    setSkillGapLoading(true);

    setSkillGapError("");



    try {

      const id = await loadStudentId();



      const response = await fetch(

        `${API_URL}/skill-gap/${id}`

      );



      const data = await response.json();



      if (!response.ok) {

        throw new Error(

          data.detail ||

            "Unable to load skill gap analysis."

        );

      }



      setSkillGapResults(

        data.results || []

      );

    } catch (error) {

      console.error(

        "Skill gap loading error:",

        error

      );



      setSkillGapError(

        error.message ||

          "Unable to load skill gap analysis."

      );



      setSkillGapResults([]);

    } finally {

      setSkillGapLoading(false);

    }

  };



  // =========================================================

  // CUSTOMIZE RESUME FOR SELECTED INTERNSHIP

  // =========================================================

  const handleCustomizeResume = async (jobId) => {

    setCareerActionLoading(`resume-${jobId}`);

    setCareerActionError("");

    setCareerActionJobId(jobId);

    setCustomizedResume(null);

    setCoverLetter("");

    try {

      const id = await loadStudentId();

      const response = await fetch(

        `${API_URL}/resume/customize?student_id=${encodeURIComponent(

          id

        )}&job_id=${encodeURIComponent(jobId)}`,

        {

          method: "POST",

        }

      );

      const data = await response.json();

      if (!response.ok) {

        throw new Error(

          data.detail || "Unable to customize your resume."

        );

      }

      setCustomizedResume(data.customized_resume || null);

    } catch (error) {

      console.error("Resume customization error:", error);

      setCareerActionError(

        error.message || "Unable to customize your resume."

      );

    } finally {

      setCareerActionLoading("");

    }

  };



  // =========================================================

  // GENERATE COVER LETTER FOR SELECTED INTERNSHIP

  // =========================================================

  const handleGenerateCoverLetter = async (jobId) => {

    setCareerActionLoading(`cover-${jobId}`);

    setCareerActionError("");

    setCareerActionJobId(jobId);

    setCustomizedResume(null);

    setCoverLetter("");

    try {

      const id = await loadStudentId();

      const response = await fetch(

        `${API_URL}/cover-letter/generate?student_id=${encodeURIComponent(

          id

        )}&job_id=${encodeURIComponent(jobId)}`,

        {

          method: "POST",

        }

      );

      const data = await response.json();

      if (!response.ok) {

        throw new Error(

          data.detail || "Unable to generate the cover letter."

        );

      }

      setCoverLetter(data.cover_letter || "");

    } catch (error) {

      console.error("Cover letter generation error:", error);

      setCareerActionError(

        error.message || "Unable to generate the cover letter."

      );

    } finally {

      setCareerActionLoading("");

    }

  };

// =========================================================
// LOAD INTERVIEW PREPARATION
// =========================================================

const loadInterviewPrep = async (jobId) => {
  setInterviewLoading(true);
  setInterviewError("");
  setInterviewPlan(null);
  setInterviewJobId(jobId);

  try {
    const id = await loadStudentId();

    const response = await fetch(
      `${API_URL}/interview-prep/${encodeURIComponent(id)}/${encodeURIComponent(jobId)}`
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Unable to generate interview preparation."
      );
    }

    setInterviewPlan(data.interview_plan || null);

  } catch (error) {
    console.error("Interview preparation error:", error);

    setInterviewError(
      error.message || "Unable to generate interview preparation."
    );

  } finally {
    setInterviewLoading(false);
  }
};

// =========================================================
// ASK AI CAREER ASSISTANT
// =========================================================

const askCareerAssistant = async (questionOverride = "") => {
  const question = (questionOverride || careerQuestion).trim();

  if (!question) {
    setCareerError("Please enter a career-related question.");
    return;
  }

  setCareerLoading(true);
  setCareerError("");
  setCareerResponse("");
  setCareerIntent("");

  try {
    const id = await loadStudentId();

    const response = await fetch(
      `${API_URL}/career-assistant/${encodeURIComponent(id)}?question=${encodeURIComponent(question)}`,
      {
        method: "POST",
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail ||
          "Unable to get a response from the AI Career Assistant."
      );
    }

    setCareerIntent(data.intent || "general");
    setCareerResponse(data.response || "No response generated.");
  } catch (error) {
    console.error("Career Assistant error:", error);

    setCareerError(
      error.message ||
        "Unable to connect to the AI Career Assistant."
    );
  } finally {
    setCareerLoading(false);
  }
};

  // =========================================================

  // LOAD DATA WHEN PAGE OPENS

  // =========================================================

  useEffect(() => {

    if (activePage === "Internships") {

      loadInternshipMatches();

    }



    if (activePage === "Skill Gap") {

      loadSkillGap();

    }

  }, [activePage]);



  // =========================================================

  // DASHBOARD

  // =========================================================

  const Dashboard = () => {

    return (

      <>

        <div className="welcome-banner">

          <div>

            <p className="small-label">

              WELCOME BACK 👋

            </p>



            <h1>

              Build your career with AI

            </h1>



            <p>

              Discover internships, identify

              skill gaps and prepare for

              interviews with your AI Career

              Companion.

            </p>

          </div>



          <div className="welcome-icon">

            ✨

          </div>

        </div>



        <div className="stats-grid">

          <div className="stat-card">

            <div className="stat-icon">

              💼

            </div>



            <div>

              <p>Internship Matches</p>



              <h2>

                {internshipMatches.length > 0

                  ? internshipMatches.length

                  : "24"}

              </h2>

            </div>

          </div>



          <div className="stat-card">

            <div className="stat-icon">

              🎯

            </div>



            <div>

              <p>Skills Matched</p>

              <h2>78%</h2>

            </div>

          </div>



          <div className="stat-card">

            <div className="stat-icon">

              📄

            </div>



            <div>

              <p>Resume Score</p>

              <h2>86%</h2>

            </div>

          </div>



          <div className="stat-card">

            <div className="stat-icon">

              🎤

            </div>



            <div>

              <p>Interview Readiness</p>

              <h2>72%</h2>

            </div>

          </div>

        </div>



        <div className="dashboard-grid">

          <div className="dashboard-card">

            <div className="card-header">

              <div>

                <h2>

                  Top Internship Matches

                </h2>



                <p>

                  Based on your profile and

                  skills

                </p>

              </div>



              <button

                className="view-btn"

                onClick={() =>

                  setActivePage(

                    "Internships"

                  )

                }

              >

                View all

              </button>

            </div>



            <div className="internship-list">

              {internshipMatches.length > 0

                ? internshipMatches

                    .slice(0, 3)

                    .map((item, index) => (

                      <div

                        className="internship-item"

                        key={index}

                      >

                        <div className="company-logo">

                          {item.company

                            ? item.company.charAt(0)

                            : "C"}

                        </div>



                        <div className="internship-info">

                          <h3>

                            {item.job_title}

                          </h3>



                          <p>

                            {item.company} •{" "}

                            {item.location}

                          </p>

                        </div>



                        <div className="match-score">

                          {item.match_score}%

                        </div>

                      </div>

                    ))

                : demoInternships.map(

                    (item, index) => (

                      <div

                        className="internship-item"

                        key={index}

                      >

                        <div className="company-logo">

                          {item.company.charAt(0)}

                        </div>



                        <div className="internship-info">

                          <h3>

                            {item.role}

                          </h3>



                          <p>

                            {item.company} •{" "}

                            {item.location}

                          </p>

                        </div>



                        <div className="match-score">

                          {item.match}

                        </div>

                      </div>

                    )

                  )}

            </div>

          </div>



          <div className="dashboard-card">

            <div className="card-header">

              <div>

                <h2>

                  Career Progress

                </h2>



                <p>

                  Your current preparation

                </p>

              </div>

            </div>



            <div className="progress-section">

              <div className="progress-row">

                <span>Resume</span>

                <strong>86%</strong>

              </div>



              <div className="progress-bar">

                <div

                  className="progress-fill"

                  style={{

                    width: "86%",

                  }}

                />

              </div>

            </div>



            <div className="progress-section">

              <div className="progress-row">

                <span>Skills</span>

                <strong>78%</strong>

              </div>



              <div className="progress-bar">

                <div

                  className="progress-fill"

                  style={{

                    width: "78%",

                  }}

                />

              </div>

            </div>



            <div className="progress-section">

              <div className="progress-row">

                <span>Interview</span>

                <strong>72%</strong>

              </div>



              <div className="progress-bar">

                <div

                  className="progress-fill"

                  style={{

                    width: "72%",

                  }}

                />

              </div>

            </div>

          </div>

        </div>



        <div className="quick-actions">

          <h2>Quick Actions</h2>



          <div className="action-grid">

            <button

              onClick={() =>

                setActivePage("Resume")

              }

            >

              <span>📄</span>



              <div>

                <strong>

                  Upload Resume

                </strong>



                <small>

                  Analyze your resume

                </small>

              </div>

            </button>



            <button

              onClick={() =>

                setActivePage("Skill Gap")

              }

            >

              <span>🎯</span>



              <div>

                <strong>

                  Check Skill Gap

                </strong>



                <small>

                  Find missing skills

                </small>

              </div>

            </button>



            <button

              onClick={() =>

                setActivePage(

                  "Interview Prep"

                )

              }

            >

              <span>🎤</span>



              <div>

                <strong>

                  Practice Interview

                </strong>



                <small>

                  Prepare for interviews

                </small>

              </div>

            </button>



            <button

              onClick={() =>

                setActivePage(

                  "AI Assistant"

                )

              }

            >

              <span>✨</span>



              <div>

                <strong>

                  Ask AI Assistant

                </strong>



                <small>

                  Get career guidance

                </small>

              </div>

            </button>

          </div>

        </div>

      </>

    );

  };



  // =========================================================

  // RESUME PAGE

  // =========================================================

  const ResumePage = () => {

    return (

      <div className="page-container">

        <div className="page-heading">

          <div>

            <p className="small-label">

              AI CAREER COMPANION

            </p>



            <h1>

              Resume Analyzer

            </h1>



            <p>

              Upload your resume and let the

              AI extract your skills,

              education, experience and

              projects.

            </p>

          </div>

        </div>



        <div className="resume-upload-card">

          <div className="upload-icon">

            📄

          </div>



          <h2>

            Upload your resume

          </h2>



          <p>

            Upload your latest resume in PDF

            format.

          </p>



          <label className="file-input-label">

            <input

              type="file"

              accept=".pdf"

              onChange={handleFileChange}

            />



            <span>

              Choose PDF Resume

            </span>

          </label>



          {selectedFile && (

            <div className="selected-file">

              <span>📎</span>



              <div>

                <strong>

                  {selectedFile.name}

                </strong>



                <small>

                  {(

                    selectedFile.size /

                    1024

                  ).toFixed(1)}{" "}

                  KB

                </small>

              </div>

            </div>

          )}



          <button

            className="upload-button"

            onClick={handleResumeUpload}

            disabled={uploading}

          >

            {uploading

              ? "Analyzing Resume..."

              : "Upload & Analyze Resume"}

          </button>



          {uploadMessage && (

            <div

              className={

                uploadMessage.includes(

                  "successfully"

                )

                  ? "success-message"

                  : "error-message"

              }

            >

              {uploadMessage}

            </div>

          )}

        </div>



        {resumeData && (

          <div className="resume-result-card">

            <div className="result-header">

              <div>

                <p className="small-label">

                  ANALYSIS COMPLETE

                </p>



                <h2>

                  Extracted Resume

                  Information

                </h2>

              </div>



              <span className="success-badge">

                ✓ Parsed

              </span>

            </div>



            <div className="resume-info-grid">

              <div className="info-box">

                <span>Name</span>



                <strong>

                  {resumeData.name ||

                    "Not detected"}

                </strong>

              </div>



              <div className="info-box">

                <span>Email</span>



                <strong>

                  {resumeData.email ||

                    "Not detected"}

                </strong>

              </div>



              <div className="info-box">

                <span>Phone</span>



                <strong>

                  {resumeData.phone ||

                    "Not detected"}

                </strong>

              </div>

            </div>



            <div className="result-section">

              <h3>Skills</h3>



              <div className="skill-tags">

                {resumeData.skills &&

                resumeData.skills.length >

                  0 ? (

                  resumeData.skills.map(

                    (skill, index) => (

                      <span

                        className="skill-tag"

                        key={index}

                      >

                        {skill}

                      </span>

                    )

                  )

                ) : (

                  <p>

                    No skills detected.

                  </p>

                )}

              </div>

            </div>



            <div className="result-section">

              <h3>Education</h3>



              {resumeData.education &&

              resumeData.education.length >

                0 ? (

                <ul>

                  {resumeData.education.map(

                    (item, index) => (

                      <li key={index}>

                        {item}

                      </li>

                    )

                  )}

                </ul>

              ) : (

                <p>

                  No education information

                  detected.

                </p>

              )}

            </div>



            <div className="result-section">

              <h3>Experience</h3>



              {resumeData.experience &&

              resumeData.experience.length >

                0 ? (

                <ul>

                  {resumeData.experience.map(

                    (item, index) => (

                      <li key={index}>

                        {item}

                      </li>

                    )

                  )}

                </ul>

              ) : (

                <p>

                  No experience information

                  detected.

                </p>

              )}

            </div>



            <div className="result-section">

              <h3>Projects</h3>



              {resumeData.projects &&

              resumeData.projects.length >

                0 ? (

                <ul>

                  {resumeData.projects.map(

                    (item, index) => (

                      <li key={index}>

                        {item}

                      </li>

                    )

                  )}

                </ul>

              ) : (

                <p>

                  No projects detected.

                </p>

              )}

            </div>



            <div className="result-section">

              <h3>Certifications</h3>



              {resumeData.certifications &&

              resumeData.certifications

                .length > 0 ? (

                <ul>

                  {resumeData.certifications.map(

                    (item, index) => (

                      <li key={index}>

                        {item}

                      </li>

                    )

                  )}

                </ul>

              ) : (

                <p>

                  No certifications

                  detected.

                </p>

              )}

            </div>

          </div>

        )}

      </div>

    );

  };



  // =========================================================

  // INTERNSHIPS PAGE

  // =========================================================

  const InternshipsPage = () => {

    return (

      <div className="page-container">

        <div className="page-heading">

          <div>

            <p className="small-label">

              M2 JOB MATCHING AGENT

            </p>



            <h1>

              Internship Matches 💼

            </h1>



            <p>

              Internships ranked using semantic

              search, skills, education,

              experience and project relevance.

            </p>

          </div>



          <button

            className="view-btn"

            onClick={loadInternshipMatches}

            disabled={internshipLoading}

          >

            {internshipLoading

              ? "Refreshing..."

              : "↻ Refresh Matches"}

          </button>

        </div>



        {!studentId &&

          !internshipLoading && (

            <div className="coming-soon-card">

              <div className="coming-icon">

                📄

              </div>



              <h2>

                Upload your resume first

              </h2>



              <p>

                Your internship matches are

                generated from your resume

                profile.

              </p>



              <button

                className="upload-button"

                onClick={() =>

                  setActivePage("Resume")

                }

              >

                Go to Resume

              </button>

            </div>

          )}



        {internshipLoading && (

          <div className="coming-soon-card">

            <div className="coming-icon">

              🔎

            </div>



            <h2>

              Finding your best matches...

            </h2>



            <p>

              Running FAISS semantic search

              and the job-resume matching

              agent.

            </p>

          </div>

        )}



        {internshipError && (

          <div className="error-message">

            {internshipError}

          </div>

        )}



        {!internshipLoading &&

          !internshipError &&

          internshipMatches.length > 0 && (

            <>

              <div className="match-summary">

                <div>

                  <strong>

                    {internshipMatches.length}

                  </strong>



                  <span>

                    internships found

                  </span>

                </div>



                <div>

                  <strong>

                    {Math.round(

                      internshipMatches.reduce(

                        (sum, item) =>

                          sum +

                          Number(

                            item.match_score ||

                              0

                          ),

                        0

                      ) /

                        internshipMatches.length

                    )}

                    %

                  </strong>



                  <span>

                    average match

                  </span>

                </div>

              </div>



              <div className="real-internship-list">

                {internshipMatches.map(

                  (item, index) => (

                    <div

                      className="real-internship-card"

                      key={

                        item.job_id ||

                        index

                      }

                    >

                      <div className="internship-card-top">

                        <div className="company-logo large">

                          {item.company

                            ? item.company.charAt(

                                0

                              )

                            : "C"}

                        </div>



                        <div className="internship-card-title">

                          <h2>

                            {item.job_title ||

                              "Internship"}

                          </h2>



                          <p>

                            {item.company ||

                              "Company"}

                            {" • "}

                            {item.location ||

                              "Location not specified"}

                          </p>

                        </div>



                        <div className="large-match-score">

                          {item.match_score}%

                          <span>

                            Match

                          </span>

                        </div>

                      </div>



                      <div className="match-details">

                        <div className="score-box">

                          <span>

                            Required Skills

                          </span>



                          <strong>

                            {item.required_skill_score ||

                              0}

                            %

                          </strong>

                        </div>



                        <div className="score-box">

                          <span>

                            Preferred Skills

                          </span>



                          <strong>

                            {item.preferred_skill_score ||

                              0}

                            %

                          </strong>

                        </div>



                        <div className="score-box">

                          <span>

                            Education

                          </span>



                          <strong>

                            {item.education_score ||

                              0}

                            %

                          </strong>

                        </div>



                        <div className="score-box">

                          <span>

                            Projects

                          </span>



                          <strong>

                            {item.project_score ||

                              0}

                            %

                          </strong>

                        </div>

                      </div>



                      <div className="skills-section">

                        <h3>

                          Matched Required

                          Skills

                        </h3>



                        <div className="skill-tags">

                          {item.matched_required_skills &&

                          item

                            .matched_required_skills

                            .length > 0 ? (

                            item.matched_required_skills.map(

                              (

                                skill,

                                skillIndex

                              ) => (

                                <span

                                  className="skill-tag"

                                  key={

                                    skillIndex

                                  }

                                >

                                  ✓ {skill}

                                </span>

                              )

                            )

                          ) : (

                            <span>

                              No required

                              skills matched

                            </span>

                          )}

                        </div>

                      </div>



                      <div className="skills-section">

                        <h3>

                          Missing Required

                          Skills

                        </h3>



                        <div className="skill-tags">

                          {item.missing_required_skills &&

                          item

                            .missing_required_skills

                            .length > 0 ? (

                            item.missing_required_skills.map(

                              (

                                skill,

                                skillIndex

                              ) => (

                                <span

                                  className="missing-skill-tag"

                                  key={

                                    skillIndex

                                  }

                                >

                                  + {skill}

                                </span>

                              )

                            )

                          ) : (

                            <span className="matched-text">

                              No major required

                              skill gaps 🎉

                            </span>

                          )}

                        </div>

                      </div>



                      {item.reasoning &&

                        item.reasoning.length >

                          0 && (

                          <div className="reasoning-section">

                            <h3>

                              Why this matches

                            </h3>



                            <ul>

                              {item.reasoning.map(

                                (

                                  reason,

                                  reasonIndex

                                ) => (

                                  <li

                                    key={

                                      reasonIndex

                                    }

                                  >

                                    {reason}

                                  </li>

                                )

                              )}

                            </ul>

                          </div>

                        )}


                      <div

                        className="career-actions"

                        style={{

                          marginTop: "24px",

                          paddingTop: "20px",

                          borderTop: "1px solid #e5e7eb",

                        }}

                      >

                        <h3 style={{ marginBottom: "12px" }}>

                          Career Documents ✨

                        </h3>



                        <div

                          style={{

                            display: "flex",

                            gap: "12px",

                            flexWrap: "wrap",

                          }}

                        >

                          <button

                            className="upload-button"

                            onClick={() =>

                              handleCustomizeResume(item.job_id)

                            }

                            disabled={

                              careerActionLoading ===

                              `resume-${item.job_id}`

                            }

                            style={{

                              width: "auto",

                              margin: 0,

                            }}

                          >

                            {careerActionLoading ===

                            `resume-${item.job_id}`

                              ? "Customizing..."

                              : "✨ Customize Resume"}

                          </button>



                          <button

                            className="view-btn"

                            onClick={() =>

                              handleGenerateCoverLetter(item.job_id)

                            }

                            disabled={

                              careerActionLoading ===

                              `cover-${item.job_id}`

                            }

                          >

                            {careerActionLoading ===

                            `cover-${item.job_id}`

                              ? "Generating..."

                              : "📝 Generate Cover Letter"}

                          </button>

                        </div>



                        {careerActionError &&

                          careerActionJobId === item.job_id && (

                          <div

                            className="error-message"

                            style={{ marginTop: "16px" }}

                          >

                            {careerActionError}

                          </div>

                        )}



                        {careerActionJobId === item.job_id &&

                          customizedResume && (

                          <div

                            className="resume-result-card"

                            style={{ marginTop: "20px" }}

                          >

                            <div className="result-header">

                              <div>

                                <p className="small-label">

                                  M3 RESUME CUSTOMIZATION

                                </p>

                                <h2>

                                  Customized Resume Draft

                                </h2>

                              </div>

                              <span className="success-badge">

                                ✓ Generated

                              </span>

                            </div>



                            <div className="result-section">

                              <h3>Professional Summary</h3>

                              <p>

                                {customizedResume.professional_summary ||

                                  "No summary generated."}

                              </p>

                            </div>



                            <div className="result-section">

                              <h3>Relevant Skills</h3>

                              <div className="skill-tags">

                                {customizedResume.relevant_skills &&

                                customizedResume.relevant_skills.length > 0 ? (

                                  customizedResume.relevant_skills.map(

                                    (skill, skillIndex) => (

                                      <span

                                        className="skill-tag"

                                        key={skillIndex}

                                      >

                                        {skill}

                                      </span>

                                    )

                                  )

                                ) : (

                                  <p>No directly matching skills found.</p>

                                )}

                              </div>

                            </div>



                            <div className="result-section">

                              <h3>Education</h3>

                              {Array.isArray(customizedResume.education) ? (

                                customizedResume.education.length > 0 ? (

                                  <ul>

                                    {customizedResume.education.map(

                                      (education, educationIndex) => (

                                        <li key={educationIndex}>

                                          {education}

                                        </li>

                                      )

                                    )}

                                  </ul>

                                ) : (

                                  <p>No education information available.</p>

                                )

                              ) : (

                                <p>

                                  {customizedResume.education ||

                                    "No education information available."}

                                </p>

                              )}

                            </div>



                            <div className="result-section">

                              <h3>Experience</h3>

                              {customizedResume.experience &&

                              customizedResume.experience.length > 0 ? (

                                <ul>

                                  {customizedResume.experience.map(

                                    (experience, experienceIndex) => (

                                      <li key={experienceIndex}>

                                        {experience}

                                      </li>

                                    )

                                  )}

                                </ul>

                              ) : (

                                <p>No experience information available.</p>

                              )}

                            </div>



                            <div className="result-section">

                              <h3>Projects</h3>

                              {customizedResume.projects &&

                              customizedResume.projects.length > 0 ? (

                                <ul>

                                  {customizedResume.projects.map(

                                    (project, projectIndex) => (

                                      <li key={projectIndex}>

                                        {project}

                                      </li>

                                    )

                                  )}

                                </ul>

                              ) : (

                                <p>No projects information available.</p>

                              )}

                            </div>

                          </div>

                        )}



                        {careerActionJobId === item.job_id &&

                          coverLetter && (

                          <div

                            className="resume-result-card"

                            style={{ marginTop: "20px" }}

                          >

                            <div className="result-header">

                              <div>

                                <p className="small-label">

                                  M3 COVER LETTER AGENT

                                </p>

                                <h2>

                                  Generated Cover Letter

                                </h2>

                              </div>

                              <span className="success-badge">

                                ✓ Generated

                              </span>

                            </div>



                            <div

                              style={{

                                whiteSpace: "pre-wrap",

                                lineHeight: 1.7,

                                padding: "8px 0",

                              }}

                            >

                              {coverLetter}

                            </div>

                          </div>

                        )}

                      </div>

                    </div>

                  )

                )}

              </div>

            </>

          )}

      </div>

    );

  };



  // =========================================================

  // SKILL GAP PAGE

  // =========================================================

  const SkillGapPage = () => {

    return (

      <div className="page-container">

        <div className="page-heading">

          <div>

            <p className="small-label">

              M3 SKILL GAP AGENT

            </p>



            <h1>

              Skill Gap Analysis 🎯

            </h1>



            <p>

              Identify the skills you already

              have, the skills you are missing,

              and what to learn next.

            </p>

          </div>



          <button

            className="view-btn"

            onClick={loadSkillGap}

            disabled={skillGapLoading}

          >

            {skillGapLoading

              ? "Analyzing..."

              : "↻ Analyze Again"}

          </button>

        </div>



        {!studentId &&

          !skillGapLoading && (

            <div className="coming-soon-card">

              <div className="coming-icon">

                📄

              </div>



              <h2>

                Upload your resume first

              </h2>



              <p>

                Your skill gap analysis is

                generated from your resume

                profile.

              </p>



              <button

                className="upload-button"

                onClick={() =>

                  setActivePage("Resume")

                }

              >

                Go to Resume

              </button>

            </div>

          )}



        {skillGapLoading && (

          <div className="coming-soon-card">

            <div className="coming-icon">

              🎯

            </div>



            <h2>

              Analyzing your skill gaps...

            </h2>



            <p>

              Comparing your resume skills

              with relevant internship

              requirements.

            </p>

          </div>

        )}



        {skillGapError && (

          <div className="error-message">

            {skillGapError}

          </div>

        )}



        {!skillGapLoading &&

          !skillGapError &&

          skillGapResults.length > 0 && (

            <>

              <div className="match-summary">

                <div>

                  <strong>

                    {skillGapResults.length}

                  </strong>



                  <span>

                    internships analyzed

                  </span>

                </div>



                <div>

                  <strong>

                    {Math.round(

                      skillGapResults.reduce(

                        (sum, item) =>

                          sum +

                          Number(

                            item.required_skill_match_percentage ||

                              0

                          ),

                        0

                      ) /

                        skillGapResults.length

                    )}

                    %

                  </strong>



                  <span>

                    average required skill match

                  </span>

                </div>

              </div>



              <div className="real-internship-list">

                {skillGapResults.map(

                  (item, index) => (

                    <div

                      className="real-internship-card"

                      key={

                        item.job_id ||

                        index

                      }

                    >

                      <div className="internship-card-top">

                        <div className="company-logo large">

                          {item.company

                            ? item.company.charAt(

                                0

                              )

                            : "C"}

                        </div>



                        <div className="internship-card-title">

                          <h2>

                            {item.job_title ||

                              "Internship"}

                          </h2>



                          <p>

                            {item.company ||

                              "Company"}

                          </p>

                        </div>



                        <div className="large-match-score">

                          {item.required_skill_match_percentage ||

                            0}

                          %

                          <span>

                            Skill Match

                          </span>

                        </div>

                      </div>



                      <div className="match-details">

                        <div className="score-box">

                          <span>

                            Required Skills

                          </span>



                          <strong>

                            {item.required_skill_match_percentage ||

                              0}

                            %

                          </strong>

                        </div>



                        <div className="score-box">

                          <span>

                            Preferred Skills

                          </span>



                          <strong>

                            {item.preferred_skill_match_percentage ||

                              0}

                            %

                          </strong>

                        </div>



                        <div className="score-box">

                          <span>

                            Required Gaps

                          </span>



                          <strong>

                            {item.missing_required_skills

                              ?.length || 0}

                          </strong>

                        </div>



                        <div className="score-box">

                          <span>

                            Preferred Gaps

                          </span>



                          <strong>

                            {item.missing_preferred_skills

                              ?.length || 0}

                          </strong>

                        </div>

                      </div>



                      <div className="skills-section">

                        <h3>

                          Matched Required Skills

                        </h3>



                        <div className="skill-tags">

                          {item.matched_required_skills &&

                          item

                            .matched_required_skills

                            .length > 0 ? (

                            item.matched_required_skills.map(

                              (

                                skill,

                                skillIndex

                              ) => (

                                <span

                                  className="skill-tag"

                                  key={

                                    skillIndex

                                  }

                                >

                                  ✓ {skill}

                                </span>

                              )

                            )

                          ) : (

                            <span>

                              No required skills

                              matched

                            </span>

                          )}

                        </div>

                      </div>



                      <div className="skills-section">

                        <h3>

                          Critical Skill Gaps

                        </h3>



                        <div className="skill-tags">

                          {item.critical_gaps &&

                          item.critical_gaps.length >

                            0 ? (

                            item.critical_gaps.map(

                              (

                                skill,

                                skillIndex

                              ) => (

                                <span

                                  className="missing-skill-tag"

                                  key={

                                    skillIndex

                                  }

                                >

                                  + {skill}

                                </span>

                              )

                            )

                          ) : (

                            <span className="matched-text">

                              No critical skill

                              gaps 🎉

                            </span>

                          )}

                        </div>

                      </div>



                      <div className="skills-section">

                        <h3>

                          Preferred Skill Gaps

                        </h3>



                        <div className="skill-tags">

                          {item.preferred_gaps &&

                          item.preferred_gaps.length >

                            0 ? (

                            item.preferred_gaps.map(

                              (

                                skill,

                                skillIndex

                              ) => (

                                <span

                                  className="missing-skill-tag"

                                  key={

                                    skillIndex

                                  }

                                >

                                  + {skill}

                                </span>

                              )

                            )

                          ) : (

                            <span className="matched-text">

                              No preferred skill

                              gaps 🎉

                            </span>

                          )}

                        </div>

                      </div>



                      {item.recommendations &&

                        item.recommendations.length >

                          0 && (

                          <div className="reasoning-section">

                            <h3>

                              Recommended Actions

                            </h3>



                            <ul>

                              {item.recommendations.map(

                                (

                                  recommendation,

                                  recommendationIndex

                                ) => (

                                  <li

                                    key={

                                      recommendationIndex

                                    }

                                  >

                                    {recommendation}

                                  </li>

                                )

                              )}

                            </ul>

                          </div>

                        )}

                    </div>

                  )

                )}

              </div>

            </>

          )}

      </div>

    );

  };

// =========================================================
// INTERVIEW PREP PAGE
// =========================================================

const InterviewPrepPage = () => {
  return (
    <div className="page-container">

      <div className="page-heading">
        <div>
          <p className="small-label">
            M3 INTERVIEW PREPARATION AGENT
          </p>

          <h1>
            Interview Preparation 🎤
          </h1>

          <p>
            Practice technical, project, role-specific and HR
            questions based on your profile and selected internship.
          </p>
        </div>
      </div>

      {/* JOB SELECTION */}

      {!studentId && (
        <div className="coming-soon-card">
          <div className="coming-icon">
            📄
          </div>

          <h2>
            Upload your resume first
          </h2>

          <p>
            Your interview preparation is generated from
            your resume profile.
          </p>

          <button
            className="upload-button"
            onClick={() => setActivePage("Resume")}
          >
            Go to Resume
          </button>
        </div>
      )}

      {studentId && internshipMatches.length === 0 && (
        <div className="coming-soon-card">
          <div className="coming-icon">
            💼
          </div>

          <h2>
            No internship matches available
          </h2>

          <p>
            Load your internship matches first and then
            select a role for interview preparation.
          </p>

          <button
            className="upload-button"
            onClick={() => setActivePage("Internships")}
          >
            View Internships
          </button>
        </div>
      )}

      {studentId && internshipMatches.length > 0 && (
        <>
          {/* SELECT INTERNSHIP */}

          <div className="resume-upload-card">

            <div className="upload-icon">
              💼
            </div>

            <h2>
              Select an Internship
            </h2>

            <p>
              Choose an internship to generate
              personalized interview questions.
            </p>

            <select
              value={interviewJobId}
              onChange={(event) => {
                setInterviewJobId(event.target.value);
                setInterviewPlan(null);
                setInterviewError("");
              }}
              style={{
                width: "100%",
                padding: "14px",
                borderRadius: "10px",
                border: "1px solid #d1d5db",
                marginTop: "16px",
                fontSize: "15px"
              }}
            >
              <option value="">
                Select an internship
              </option>

              {internshipMatches.map((job) => (
                <option
                  key={job.job_id}
                  value={job.job_id}
                >
                  {job.job_title} — {job.company}
                </option>
              ))}
            </select>

            <button
              className="upload-button"
              style={{ marginTop: "16px" }}
              disabled={
                !interviewJobId ||
                interviewLoading
              }
              onClick={() =>
                loadInterviewPrep(interviewJobId)
              }
            >
              {interviewLoading
                ? "Generating Questions..."
                : "🎤 Generate Interview Preparation"}
            </button>

          </div>

          {/* ERROR */}

          {interviewError && (
            <div
              className="error-message"
              style={{ marginTop: "20px" }}
            >
              {interviewError}
            </div>
          )}

          {/* INTERVIEW PLAN */}

          {interviewPlan && (
            <div className="resume-result-card">

              <div className="result-header">

                <div>
                  <p className="small-label">
                    M3 INTERVIEW AGENT
                  </p>

                  <h2>
                    Interview Preparation Plan
                  </h2>
                </div>

                <span className="success-badge">
                  ✓ Generated
                </span>

              </div>

              {/* ROLE */}

              <div className="result-section">

                <h3>
                  🎯 Target Role
                </h3>

                <p>
                  <strong>
                    {interviewPlan.job_title}
                  </strong>
                </p>

                <p>
                  {interviewPlan.company}
                </p>

              </div>

              {/* TECHNICAL QUESTIONS */}

              <div className="result-section">

                <h3>
                  💻 Technical Questions
                </h3>

                {interviewPlan.technical_questions &&
                interviewPlan.technical_questions.length > 0 ? (

                  <ol>
                    {interviewPlan.technical_questions.map(
                      (question, index) => (
                        <li key={index}>
                          {question}
                        </li>
                      )
                    )}
                  </ol>

                ) : (
                  <p>
                    No technical questions generated.
                  </p>
                )}

              </div>

              {/* PROJECT QUESTIONS */}

              <div className="result-section">

                <h3>
                  🛠️ Project Questions
                </h3>

                {interviewPlan.project_questions &&
                interviewPlan.project_questions.length > 0 ? (

                  <ol>
                    {interviewPlan.project_questions.map(
                      (question, index) => (
                        <li key={index}>
                          {question}
                        </li>
                      )
                    )}
                  </ol>

                ) : (
                  <p>
                    No project questions available
                    from the current student profile.
                  </p>
                )}

              </div>

              {/* ROLE QUESTIONS */}

              <div className="result-section">

                <h3>
                  💼 Role-Specific Questions
                </h3>

                {interviewPlan.role_questions &&
                interviewPlan.role_questions.length > 0 ? (

                  <ol>
                    {interviewPlan.role_questions.map(
                      (question, index) => (
                        <li key={index}>
                          {question}
                        </li>
                      )
                    )}
                  </ol>

                ) : (
                  <p>
                    No role-specific questions generated.
                  </p>
                )}

              </div>

              {/* HR QUESTIONS */}

              <div className="result-section">

                <h3>
                  🧑‍💼 HR & Behavioral Questions
                </h3>

                {interviewPlan.hr_questions &&
                interviewPlan.hr_questions.length > 0 ? (

                  <ol>
                    {interviewPlan.hr_questions.map(
                      (question, index) => (
                        <li key={index}>
                          {question}
                        </li>
                      )
                    )}
                  </ol>

                ) : (
                  <p>
                    No HR questions generated.
                  </p>
                )}

              </div>

              {/* PREPARATION TIPS */}

              <div className="reasoning-section">

                <h3>
                  💡 Preparation Tips
                </h3>

                {interviewPlan.preparation_tips &&
                interviewPlan.preparation_tips.length > 0 ? (

                  <ul>
                    {interviewPlan.preparation_tips.map(
                      (tip, index) => (
                        <li key={index}>
                          {tip}
                        </li>
                      )
                    )}
                  </ul>

                ) : (
                  <p>
                    No preparation tips available.
                  </p>
                )}

              </div>

            </div>
          )}
        </>
      )}

    </div>
  );
};

  // =========================================================

  // PLACEHOLDER PAGES

  // =========================================================

  const PlaceholderPage = ({

    title,

    icon,

    description,

  }) => {

    return (

      <div className="page-container">

        <div className="page-heading">

          <div>

            <p className="small-label">

              CAREERAI MODULE

            </p>



            <h1>

              {icon} {title}

            </h1>



            <p>

              {description}

            </p>

          </div>

        </div>



        <div className="coming-soon-card">

          <div className="coming-icon">

            {icon}

          </div>



          <h2>{title}</h2>



          <p>

            This module is ready to be

            connected to your M2 and M3

            backend agents.

          </p>



          <span>

            Coming next 🚀

          </span>

        </div>

      </div>

    );

  };



  // =========================================================

  // PAGE CONTENT

  // =========================================================

  const renderPage = () => {

    switch (activePage) {

      case "Dashboard":

        return <Dashboard />;



      case "Resume":

        return <ResumePage />;



      case "My Profile":

        return (

          <PlaceholderPage

            title="My Profile"

            icon="👤"

            description="Manage your personal information, education, skills and career preferences."

          />

        );



      case "Internships":

        return <InternshipsPage />;



      case "Skill Gap":

        return <SkillGapPage />;


      case "Interview Prep":
  return <InterviewPrepPage />;






      case "AI Assistant":

        return (

          <div className="page-container">

            <div className="page-heading">

              <div>

                <p className="small-label">
                  M3 AI CAREER ASSISTANT
                </p>

                <h1>
                  ✨ AI Career Assistant
                </h1>

                <p>
                  Ask questions about internships, skill gaps,
                  resumes, cover letters and interview preparation.
                </p>

              </div>

            </div>

            <div className="resume-upload-card">

              <div className="upload-icon">
                ✨
              </div>

              <h2>
                Ask your Career Assistant
              </h2>

              <p>
                Your answer is generated using your student profile
                and internship matching data.
              </p>

              <textarea
                value={careerQuestion}
                onChange={(event) => {
                  setCareerQuestion(event.target.value);
                  setCareerError("");
                }}
                placeholder="Example: What skills am I missing?"
                rows={5}
                style={{
                  width: "100%",
                  boxSizing: "border-box",
                  padding: "14px",
                  borderRadius: "10px",
                  border: "1px solid #d1d5db",
                  marginTop: "16px",
                  fontSize: "15px",
                  resize: "vertical",
                  fontFamily: "inherit",
                  outline: "none"
                }}
              />

              <button
                className="upload-button"
                style={{ marginTop: "16px" }}
                onClick={() => askCareerAssistant()}
                disabled={
                  careerLoading ||
                  !careerQuestion.trim()
                }
              >
                {careerLoading
                  ? "Thinking..."
                  : "✨ Ask AI Assistant"}
              </button>

              <div style={{ marginTop: "20px" }}>

                <p
                  style={{
                    fontWeight: "600",
                    marginBottom: "10px"
                  }}
                >
                  Try asking:
                </p>

                <div
                  style={{
                    display: "flex",
                    gap: "10px",
                    flexWrap: "wrap"
                  }}
                >

                  {[
                    "What skills am I missing?",
                    "Which internships match my profile?",
                    "How should I prepare for an interview?",
                    "How can I improve my resume?",
                    "What should I include in my cover letter?"
                  ].map((question, index) => (

                    <button
                      key={index}
                      className="view-btn"
                      onClick={() => {
                        setCareerQuestion(question);
                        askCareerAssistant(question);
                      }}
                      disabled={careerLoading}
                      style={{
                        margin: 0,
                        cursor: careerLoading
                          ? "not-allowed"
                          : "pointer"
                      }}
                    >
                      {question}
                    </button>

                  ))}

                </div>

              </div>

            </div>

            {careerError && (

              <div
                className="error-message"
                style={{ marginTop: "20px" }}
              >
                {careerError}
              </div>

            )}

            {careerResponse && (

              <div
                className="resume-result-card"
                style={{ marginTop: "20px" }}
              >

                <div className="result-header">

                  <div>

                    <p className="small-label">
                      AI CAREER ASSISTANT
                    </p>

                    <h2>
                      Career Guidance
                    </h2>

                  </div>

                  <span className="success-badge">
                    ✓ {careerIntent || "general"}
                  </span>

                </div>

                <div
                  className="result-section"
                  style={{
                    whiteSpace: "pre-wrap",
                    lineHeight: 1.7
                  }}
                >

                  <h3>
                    🤖 Assistant Response
                  </h3>

                  <p>
                    {careerResponse}
                  </p>

                </div>

              </div>

            )}

          </div>

        );



      default:

        return <Dashboard />;

    }

  };



  // =========================================================

  // MAIN UI

  // =========================================================

  return (

    <div className="app">



      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="logo-section">

          <div className="logo-icon">

            ✨

          </div>



          <div>

            <h2>CareerAI</h2>



            <span>

              Career Companion

            </span>

          </div>

        </div>



        <nav className="sidebar-nav">

          <p className="nav-label">

            MENU

          </p>



          {menuItems.map((item) => (

            <button

              key={item.name}

              className={

                activePage === item.name

                  ? "nav-item active"

                  : "nav-item"

              }

              onClick={() =>

                setActivePage(item.name)

              }

            >

              <span className="nav-icon">

                {item.icon}

              </span>



              <span>

                {item.name}

              </span>

            </button>

          ))}

        </nav>



        <div className="sidebar-bottom">

          <div className="ai-card">

            <div className="ai-card-icon">

              ✨

            </div>



            <div>

              <strong>

                AI Career Coach

              </strong>



              <p>

                Ready to help you grow.

              </p>

            </div>

          </div>

        </div>

      </aside>



      {/* MAIN AREA */}

      <main className="main-content">



        {/* TOP BAR */}

        <header className="topbar">

          <div>

            <span className="breadcrumb">

              CareerAI

            </span>



            <span className="breadcrumb-separator">

              /

            </span>



            <strong>

              {activePage}

            </strong>

          </div>



          <div className="profile-area">

            <div className="notification">

              🔔

            </div>



            <div className="profile-avatar">

              LG

            </div>



            <div className="profile-name">

              <strong>

                Likhita

              </strong>



              <span>

                Student

              </span>

            </div>

          </div>

        </header>



        {/* PAGE */}

        <section className="content-area">

          {renderPage()}

        </section>

      </main>

    </div>

  );

}



export default App;
