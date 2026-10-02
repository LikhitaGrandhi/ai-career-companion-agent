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
  // PROFILE STATES
  // =========================================================

  const [studentProfile, setStudentProfile] = useState(null);
  const [profileLoading, setProfileLoading] = useState(false);
  const [profileError, setProfileError] = useState("");



  // =========================================================

  // INTERNSHIP STATES

  // =========================================================

  const [internshipMatches, setInternshipMatches] = useState([]);

  const [internshipLoading, setInternshipLoading] = useState(false);

  const [internshipError, setInternshipError] = useState("");

  const [customizedResume, setCustomizedResume] = useState(null);
  const [coverLetter, setCoverLetter] = useState("");
  const [generatedResumeId, setGeneratedResumeId] = useState(
  () => localStorage.getItem("generated_resume_id") || null
);

const [generatedCoverLetterId, setGeneratedCoverLetterId] = useState(
  () => localStorage.getItem("generated_cover_letter_id") || null
);

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
// M4 — Application Tracker
const [applications, setApplications] = useState([]);
const [upcomingDeadlines, setUpcomingDeadlines] = useState([]);
const [applicationLoading, setApplicationLoading] = useState(false);
const [applicationError, setApplicationError] = useState("");

const [applicationFilter, setApplicationFilter] = useState("All");
const [applicationView, setApplicationView] = useState("All");
const [applicationSearch, setApplicationSearch] = useState("");
const [showApplicationForm, setShowApplicationForm] = useState(false);

const [newApplication, setNewApplication] = useState({
  company_name: "",
  job_title: "",
  job_description: "",
  application_date: "",
  deadline: "",
  status: "Saved",
  interview_date: "",
  interview_status: "",
  notes: "",
  resume_id: null,
  cover_letter_id: null
});

// M4 — Application Dashboard
const [applicationDashboard, setApplicationDashboard] = useState({
  total_applications: 0,
  active_applications: 0,
  interviews_scheduled: 0,
  offers_received: 0,
  rejected_applications: 0
});

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
  { name: "Application Tracker", icon: "📋" },
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
  // LOAD STUDENT PROFILE
  // =========================================================

  const loadStudentProfile = async () => {
    setProfileLoading(true);
    setProfileError("");

    try {
      const id = await loadStudentId();
      const response = await fetch(`${API_URL}/students`);

      if (!response.ok) {
        throw new Error("Unable to load student profiles.");
      }

      const students = await response.json();
      const profile = (students || []).find(
        (student) => student._id === id
      );

      if (!profile) {
        throw new Error("Student profile not found.");
      }

      setStudentProfile(profile);
    } catch (error) {
      console.error("Profile loading error:", error);
      setProfileError(error.message || "Unable to load your profile.");
      setStudentProfile(null);
    } finally {
      setProfileLoading(false);
    }
  };

  useEffect(() => {
    if (activePage === "My Profile") {
      loadStudentProfile();
    }
  }, [activePage]);

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

setCoverLetter("");
setGeneratedCoverLetterId(null);
localStorage.removeItem("generated_cover_letter_id");

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

const resumeId = data.resume_id || null;

setGeneratedResumeId(resumeId);

if (resumeId) {
  localStorage.setItem("generated_resume_id", resumeId);

  setNewApplication((prev) => ({
    ...prev,
    resume_id: resumeId
  }));
}

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

const coverLetterId = data.cover_letter_id || null;

setGeneratedCoverLetterId(coverLetterId);

if (coverLetterId) {
  localStorage.setItem("generated_cover_letter_id", coverLetterId);

  setNewApplication((prev) => ({
    ...prev,
    cover_letter_id: coverLetterId
  }));
}

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
// M4 — Load Application Tracker data
const loadApplications = async (statusFilter = "") => {
  setApplicationLoading(true);
  setApplicationError("");

  try {
    const id = await loadStudentId();

    let url = `${API_URL}/applications/${encodeURIComponent(id)}`;

    if (statusFilter && statusFilter !== "All") {
      url += `?status=${encodeURIComponent(statusFilter)}`;
    }

    const response = await fetch(url);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Unable to load applications."
      );
    }

    const loadedApplications = data.applications || [];

setApplications(loadedApplications);
calculateUpcomingDeadlines(loadedApplications);
  } catch (error) {
    console.error("Application Tracker error:", error);
    setApplicationError(
      error.message || "Unable to load applications."
    );
  } finally {
    setApplicationLoading(false);
  }
};
const calculateUpcomingDeadlines = (applicationList) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const upcoming = applicationList
    .filter((application) => {
      if (!application.deadline) return false;

      const deadline = new Date(application.deadline);
      deadline.setHours(0, 0, 0, 0);

      return deadline >= today;
    })
    .sort(
      (a, b) =>
        new Date(a.deadline) - new Date(b.deadline)
    );

  setUpcomingDeadlines(upcoming);
};
useEffect(() => {
  calculateUpcomingDeadlines(applications);
}, [applications]);

// Restore generated career documents whenever the user enters a page.
// This keeps the generated Resume/Cover Letter connected to the
// Application Tracker even after navigation or a page refresh.
useEffect(() => {
  const storedResumeId = localStorage.getItem("generated_resume_id");
  const storedCoverLetterId = localStorage.getItem("generated_cover_letter_id");

  if (storedResumeId) {
    setGeneratedResumeId(storedResumeId);
  }

  if (storedCoverLetterId) {
    setGeneratedCoverLetterId(storedCoverLetterId);
  }

  if (activePage === "Application Tracker") {
    setNewApplication((prev) => ({
      ...prev,
      resume_id: prev.resume_id || storedResumeId || null,
      cover_letter_id: prev.cover_letter_id || storedCoverLetterId || null
    }));
  }
}, [activePage]);
// M4 — Load Application Dashboard
const loadApplicationDashboard = async () => {
  try {
    const id = await loadStudentId();

    const response = await fetch(
      `${API_URL}/applications/${encodeURIComponent(id)}/dashboard`
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Unable to load application dashboard."
      );
    }

    setApplicationDashboard({
      total_applications: data.total_applications || 0,
      active_applications: data.active_applications || 0,
      interviews_scheduled: data.interviews_scheduled || 0,
      offers_received: data.offers_received || 0,
      rejected_applications: data.rejected_applications || 0
    });
  } catch (error) {
    console.error("Application Dashboard error:", error);
  }
};

// M4 — Add a new application
const addApplication = async () => {
  setApplicationLoading(true);
  setApplicationError("");

  try {
    const id = await loadStudentId();

    const response = await fetch(
      `${API_URL}/applications/${encodeURIComponent(id)}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          ...newApplication,
          interview_date: newApplication.interview_date || null
        })
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Unable to add application."
      );
    }

    setShowApplicationForm(false);

    setNewApplication({
      company_name: "",
      job_title: "",
      job_description: "",
      application_date: "",
      deadline: "",
      status: "Saved",
      interview_date: "",
      interview_status: "",
      notes: "",
      resume_id: null,
      cover_letter_id: null
    });

    await loadApplications(applicationFilter);
    await loadApplicationDashboard();
  } catch (error) {
    console.error("Add application error:", error);
    setApplicationError(
      error.message || "Unable to add application."
    );
  } finally {
    setApplicationLoading(false);
  }
};
// M4 — Update an application
const updateApplication = async (applicationId, updates) => {
  setApplicationLoading(true);
  setApplicationError("");

  try {
    const id = await loadStudentId();

    const response = await fetch(
      `${API_URL}/application/${encodeURIComponent(id)}/${encodeURIComponent(applicationId)}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(updates)
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Unable to update application."
      );
    }

    await loadApplications(applicationFilter);
    await loadApplicationDashboard();
  } catch (error) {
    console.error("Update application error:", error);
    setApplicationError(
      error.message || "Unable to update application."
    );
  } finally {
    setApplicationLoading(false);
  }
};
// M4 — Delete an application
const deleteApplication = async (applicationId) => {
  const confirmed = window.confirm(
    "Are you sure you want to delete this application?"
  );

  if (!confirmed) {
    return;
  }

  setApplicationLoading(true);
  setApplicationError("");

  try {
    const id = await loadStudentId();

    const response = await fetch(
      `${API_URL}/application/${encodeURIComponent(id)}/${encodeURIComponent(applicationId)}`,
      {
        method: "DELETE"
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Unable to delete application."
      );
    }

    await loadApplications(applicationFilter);
    await loadApplicationDashboard();
  } catch (error) {
    console.error("Delete application error:", error);
    setApplicationError(
      error.message || "Unable to delete application."
    );
  } finally {
    setApplicationLoading(false);
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
     
  if (activePage === "Application Tracker") {
  loadApplications(applicationFilter);
  loadApplicationDashboard();
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

  // =========================================================
  // MY PROFILE PAGE
  // =========================================================

  const ProfilePage = () => {
    const cleanText = (value) => {
      if (!value) return "";

      return String(value)
        .replace(/◦/g, "")
        .replace(/T ech/g, "Tech")
        .replace(/W ebsite/g, "Website")
        .replace(/F or W omen/g, "for Women")
        .replace(/Artifical/g, "Artificial")
        .replace(/\s+/g, " ")
        .trim();
    };

    const formatList = (value) => {
      if (Array.isArray(value)) {
        return value
          .filter(Boolean)
          .map((item) => cleanText(item))
          .filter(Boolean);
      }

      if (typeof value === "string" && value.trim()) {
        return value
          .split(/[,;|]/)
          .map((item) => cleanText(item))
          .filter(Boolean);
      }

      return [];
    };

    const skills = formatList(studentProfile?.skills);
    const education = formatList(studentProfile?.education);
    const experience = formatList(studentProfile?.experience);
    const projects = formatList(studentProfile?.projects);
    const certifications = formatList(studentProfile?.certifications);

    const pageHeader = (
      <div className="page-heading">
        <div>
          <p className="small-label">CAREERAI MODULE</p>
          <h1>👤 My Profile</h1>
          <p>
            View your personal information, education, skills and career
            profile.
          </p>
        </div>
      </div>
    );

    if (profileLoading) {
      return (
        <div className="page-container">
          {pageHeader}

          <div className="coming-soon-card">
            <div className="coming-icon">👤</div>
            <h2>Loading Profile...</h2>
            <p>Fetching your profile information from CareerAI.</p>
          </div>
        </div>
      );
    }

    if (profileError) {
      return (
        <div className="page-container">
          {pageHeader}

          <div className="coming-soon-card">
            <div className="coming-icon">⚠️</div>
            <h2>Unable to load profile</h2>
            <p>{profileError}</p>

            <button
              className="upload-button"
              onClick={loadStudentProfile}
              style={{ marginTop: "15px" }}
            >
              Try Again
            </button>
          </div>
        </div>
      );
    }

    if (!studentProfile) {
      return (
        <div className="page-container">
          {pageHeader}

          <div className="coming-soon-card">
            <div className="coming-icon">📄</div>
            <h2>No Profile Found</h2>
            <p>
              Upload your resume first to create your student profile.
            </p>

            <button
              className="upload-button"
              onClick={() => setActivePage("Resume")}
              style={{ marginTop: "15px" }}
            >
              Go to Resume
            </button>
          </div>
        </div>
      );
    }

    const renderList = (items, emptyText) => {
      if (items.length === 0) {
        return <p>{emptyText}</p>;
      }

      return (
        <div style={{ marginTop: "15px" }}>
          {items.map((item, index) => (
            <div
              key={index}
              style={{
                padding: "12px 15px",
                marginBottom: "10px",
                borderRadius: "10px",
                background: "#f8fafc",
                border: "1px solid #e5e7eb",
                lineHeight: 1.6
              }}
            >
              {item}
            </div>
          ))}
        </div>
      );
    };

    return (
      <div className="page-container">
        {pageHeader}

        {/* PERSONAL INFORMATION */}
        <div
          className="result-card"
          style={{
            marginBottom: "20px"
          }}
        >
          <p className="small-label">PERSONAL INFORMATION</p>

          <h2 style={{ margin: "8px 0 18px", fontSize: "26px" }}>
            {cleanText(studentProfile.name) || "Name not provided"}
          </h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
              gap: "12px"
            }}
          >
            <p style={{ margin: 0 }}>
              <strong>Email:</strong>{" "}
              {studentProfile.email || "Not provided"}
            </p>

            <p style={{ margin: 0 }}>
              <strong>Phone:</strong>{" "}
              {studentProfile.phone || "Not provided"}
            </p>
          </div>
        </div>

        {/* PROFILE ID */}
        <div
          className="result-card"
          style={{
            marginBottom: "20px"
          }}
        >
          <p className="small-label">PROFILE ID</p>

          <p
            style={{
              marginTop: "8px",
              wordBreak: "break-all",
              fontFamily: "monospace"
            }}
          >
            {studentProfile._id || "Not available"}
          </p>
        </div>

        {/* EDUCATION */}
        <div
          className="result-card"
          style={{
            marginBottom: "20px"
          }}
        >
          <h2>🎓 Education</h2>
          {renderList(education, "No education details available.")}
        </div>

        {/* SKILLS */}
        <div
          className="result-card"
          style={{
            marginBottom: "20px"
          }}
        >
          <h2>💻 Skills</h2>

          {skills.length > 0 ? (
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "10px",
                marginTop: "16px"
              }}
            >
              {skills.map((skill, index) => (
                <span
                  key={index}
                  style={{
                    display: "inline-block",
                    padding: "9px 15px",
                    borderRadius: "20px",
                    background: "#eef2ff",
                    border: "1px solid #dbe3ff",
                    fontSize: "14px",
                    fontWeight: "600"
                  }}
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p>No skills available.</p>
          )}
        </div>

        {/* EXPERIENCE */}
        <div
          className="result-card"
          style={{
            marginBottom: "20px"
          }}
        >
          <h2>💼 Experience</h2>
          {renderList(experience, "No experience details available.")}
        </div>

        {/* PROJECTS */}
        <div
          className="result-card"
          style={{
            marginBottom: "20px"
          }}
        >
          <h2>🚀 Projects</h2>
          {renderList(projects, "No project details available.")}
        </div>

        {/* CERTIFICATIONS */}
        <div
          className="result-card"
          style={{
            marginBottom: "20px"
          }}
        >
          <h2>🏆 Certifications</h2>
          {renderList(certifications, "No certifications available.")}
        </div>
      </div>
    );
  };

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
        return <ProfilePage />;



      case "Internships":

        return <InternshipsPage />;



      case "Skill Gap":

        return <SkillGapPage />;


      case "Interview Prep":
  return <InterviewPrepPage />;
        case "Application Tracker":

        return (
          <div className="page-container">

            <div className="page-heading">
              <div>
                <p className="small-label">
                  M4 APPLICATION TRACKER
                </p>
                <h1>Application Tracker</h1>
                <p>
                  Track internships, applications, deadlines,
                  interviews and follow-up notes in one place.
                </p>
              </div>

              <button
                className="primary-button"
                onClick={() => setShowApplicationForm(true)}
              >
                + Add Application
              </button>
            </div>

            {applicationError && (
              <div className="error-message">
                {applicationError}
              </div>
            )}

            {/* APPLICATION DASHBOARD */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(5, minmax(0, 1fr))",
                gap: "15px",
                marginBottom: "25px"
              }}
            >
              <div className="stat-card">
                <div className="stat-icon">📋</div>
                <div>
                  <p>Total Applications</p>
                  <h2>{applicationDashboard.total_applications}</h2>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">📈</div>
                <div>
                  <p>Active Applications</p>
                  <h2>{applicationDashboard.active_applications}</h2>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">🎤</div>
                <div>
                  <p>Interviews Scheduled</p>
                  <h2>{applicationDashboard.interviews_scheduled}</h2>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">🎉</div>
                <div>
                  <p>Offers Received</p>
                  <h2>{applicationDashboard.offers_received}</h2>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">❌</div>
                <div>
                  <p>Rejected</p>
                  <h2>{applicationDashboard.rejected_applications}</h2>
                </div>
              </div>
            </div>

            <div className="application-tracker-content">
              {/* UPCOMING DEADLINES */}
{upcomingDeadlines.length > 0 && (
  <div
    className="coming-soon-card"
    style={{
      marginBottom: "20px",
      textAlign: "left"
    }}
  >
    <h2>📅 Upcoming Deadlines</h2>

    <p style={{ marginBottom: "15px" }}>
      Applications with upcoming deadlines.
    </p>

    <div
      style={{
        display: "grid",
        gap: "12px"
      }}
    >
      {upcomingDeadlines.map((application) => {
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const deadline = new Date(application.deadline);
        deadline.setHours(0, 0, 0, 0);

        const daysLeft = Math.ceil(
          (deadline - today) / (1000 * 60 * 60 * 24)
        );

        return (
          <div
            key={application.id}
            style={{
              padding: "14px",
              border: "1px solid #e5e7eb",
              borderRadius: "10px",
              background: "#fafafa"
            }}
          >
            <strong>
              {application.company_name}
            </strong>

            <div style={{ marginTop: "5px" }}>
              {application.job_title}
            </div>

            <div
              style={{
                marginTop: "8px",
                fontSize: "14px"
              }}
            >
              📅 Deadline: {application.deadline}
            </div>

            <div
              style={{
                marginTop: "5px",
                fontSize: "14px",
                fontWeight: "600"
              }}
            >
              ⏳{" "}
              {daysLeft === 0
                ? "Due today"
                : daysLeft === 1
                ? "1 day remaining"
                : `${daysLeft} days remaining`}
            </div>
          </div>
        );
      })}
    </div>
  </div>
)}

             
              {/* FILTER + SEARCH */}
<div
  style={{
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "15px",
    marginBottom: "20px",
    flexWrap: "wrap"
  }}
>
  {/* Search */}
  <input
    type="text"
    placeholder="Search company or role..."
    value={applicationSearch}
    onChange={(e) => setApplicationSearch(e.target.value)}
    style={{
      flex: "1",
      minWidth: "250px",
      padding: "10px 12px",
      borderRadius: "8px",
      border: "1px solid #d1d5db",
      fontSize: "14px"
    }}
  />

  {/* Status Filter + Active/Completed View */}
  <div
    style={{
      display: "flex",
      alignItems: "center",
      gap: "10px",
      flexWrap: "wrap"
    }}
  >
    <label>
      <strong>Filter:</strong>
    </label>

    <select
      value={applicationFilter}
      onChange={(e) => {
        const value = e.target.value;
        setApplicationFilter(value);
        loadApplications(value);
      }}
      style={{
        padding: "9px 12px",
        borderRadius: "8px",
        border: "1px solid #d1d5db"
      }}
    >
      <option value="All">All Applications</option>
      <option value="Saved">Saved</option>
      <option value="Planning to apply">Planning to apply</option>
      <option value="Applied">Applied</option>
      <option value="Application under review">
        Application under review
      </option>
      <option value="Shortlisted">Shortlisted</option>
      <option value="Interview scheduled">
        Interview scheduled
      </option>
      <option value="Interview completed">
        Interview completed
      </option>
      <option value="Offer received">Offer received</option>
      <option value="Rejected">Rejected</option>
      <option value="Withdrawn">Withdrawn</option>
    </select>

    <label style={{ marginLeft: "10px" }}>
      <strong>View:</strong>
    </label>

    <select
      value={applicationView}
      onChange={(e) => setApplicationView(e.target.value)}
      style={{
        padding: "9px 12px",
        borderRadius: "8px",
        border: "1px solid #d1d5db"
      }}
    >
      <option value="All">All</option>
      <option value="Active">Active</option>
      <option value="Completed">Completed</option>
    </select>
  </div>
</div>

              {/* ADD APPLICATION FORM */}
              {showApplicationForm && (
                <div className="coming-soon-card">
                  <h2>Add New Application</h2>
                  <p>Enter the details of the internship or job application.</p>

                  <div
                    style={{
                      display: "grid",
                      gap: "14px",
                      marginTop: "20px",
                      textAlign: "left"
                    }}
                  >
                    <input
                      type="text"
                      placeholder="Company Name"
                      value={newApplication.company_name}
                      onChange={(e) =>
                        setNewApplication({
                          ...newApplication,
                          company_name: e.target.value
                        })
                      }
                    />

                    <input
                      type="text"
                      placeholder="Job / Internship Title"
                      value={newApplication.job_title}
                      onChange={(e) =>
                        setNewApplication({
                          ...newApplication,
                          job_title: e.target.value
                        })
                      }
                    />

                    <textarea
                      placeholder="Job Description"
                      value={newApplication.job_description}
                      onChange={(e) =>
                        setNewApplication({
                          ...newApplication,
                          job_description: e.target.value
                        })
                      }
                      rows="4"
                    />

                    <label>Application Date</label>
                    <input
                      type="date"
                      value={newApplication.application_date}
                      onChange={(e) =>
                        setNewApplication({
                          ...newApplication,
                          application_date: e.target.value
                        })
                      }
                    />

                    <label>Application Deadline</label>
                    <input
                      type="date"
                      value={newApplication.deadline}
                      onChange={(e) =>
                        setNewApplication({
                          ...newApplication,
                          deadline: e.target.value
                        })
                      }
                    />

                    <label>Application Status</label>
                    <select
                      value={newApplication.status}
                      onChange={(e) =>
                        setNewApplication({
                          ...newApplication,
                          status: e.target.value
                        })
                      }
                    >
                      <option value="Saved">Saved</option>
                      <option value="Planning to apply">Planning to apply</option>
                      <option value="Applied">Applied</option>
                      <option value="Application under review">Application under review</option>
                      <option value="Shortlisted">Shortlisted</option>
                      <option value="Interview scheduled">Interview scheduled</option>
                      <option value="Interview completed">Interview completed</option>
                      <option value="Offer received">Offer received</option>
                      <option value="Rejected">Rejected</option>
                      <option value="Withdrawn">Withdrawn</option>
                    </select>

                    <label>Interview Date</label>
                    <input
                      type="date"
                      value={newApplication.interview_date}
                      onChange={(e) =>
                        setNewApplication({
                          ...newApplication,
                          interview_date: e.target.value
                        })
                      }
                    />

                    <label>Interview Status</label>
                    <select
                      value={newApplication.interview_status}
                      onChange={(e) =>
                        setNewApplication({
                          ...newApplication,
                          interview_status: e.target.value
                        })
                      }
                    >
                      <option value="">Not scheduled</option>
                      <option value="Scheduled">Scheduled</option>
                      <option value="Completed">Completed</option>
                      <option value="Cancelled">Cancelled</option>
                    </select>

                   <label>Resume</label>

<select
  value={newApplication.resume_id || ""}
  onChange={(e) =>
    setNewApplication({
      ...newApplication,
      resume_id: e.target.value || null
    })
  }
>
  <option value="">No resume selected</option>

  {generatedResumeId && (
    <option value={generatedResumeId}>
      Current Generated Resume
    </option>
  )}
</select>
<label>Cover Letter</label>

<select
  value={newApplication.cover_letter_id || ""}
  onChange={(e) =>
    setNewApplication({
      ...newApplication,
      cover_letter_id: e.target.value || null
    })
  }
>
  <option value="">No cover letter selected</option>

  {generatedCoverLetterId && (
    <option value={generatedCoverLetterId}>
      Current Generated Cover Letter
    </option>
  )}
</select>
                    <textarea
                      placeholder="Notes / Follow-up"
                      value={newApplication.notes}
                      onChange={(e) =>
                        setNewApplication({
                          ...newApplication,
                          notes: e.target.value
                        })
                      }
                      rows="3"
                    />
                  </div>

                  <div
                    style={{
                      display: "flex",
                      gap: "12px",
                      marginTop: "20px"
                    }}
                  >
                    <button
                      className="upload-button"
                      onClick={addApplication}
                      disabled={
                        applicationLoading ||
                        !newApplication.company_name.trim() ||
                        !newApplication.job_title.trim()
                      }
                    >
                      {applicationLoading ? "Adding..." : "Add Application"}
                    </button>

                    <button
                      className="view-btn"
                      onClick={() => setShowApplicationForm(false)}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}

              {/* APPLICATION LIST */}
              {applicationLoading ? (
                <div className="coming-soon-card">
                  <div className="coming-icon">📋</div>
                  <h2>Loading applications...</h2>
                  <p>Fetching your application tracker data.</p>
                </div>
              ) : applications.length === 0 ? (
                <div className="coming-soon-card">
                  <div className="coming-icon">📋</div>
                  <h2>No applications yet</h2>
                  <p>
                    Add an internship or job application to start tracking your applications.
                  </p>
                  <button
                    className="upload-button"
                    onClick={() => setShowApplicationForm(true)}
                  >
                    + Add Application
                  </button>
                </div>
              ) : (
                <div className="real-internship-list">
                  {applications
  .filter((application) => {
    const search = applicationSearch.toLowerCase().trim();

    const matchesSearch =
      !search ||
      application.company_name
        ?.toLowerCase()
        .includes(search) ||
      application.job_title
        ?.toLowerCase()
        .includes(search);

    const completedStatuses = [
      "Offer received",
      "Rejected",
      "Withdrawn"
    ];

    const matchesView =
      applicationView === "All" ||
      (applicationView === "Completed" &&
        completedStatuses.includes(application.status)) ||
      (applicationView === "Active" &&
        !completedStatuses.includes(application.status));

    return matchesSearch && matchesView;
  })
  .map((application) => (
                    <div
                      className="real-internship-card"
                      key={application.id}
                    >
                      <div className="internship-card-top">
                        <div className="company-logo large">
                          {application.company_name
                            ? application.company_name.charAt(0).toUpperCase()
                            : "C"}
                        </div>

                        <div className="internship-card-title">
                          <h2>{application.job_title}</h2>
                          <p>{application.company_name}</p>
                        </div>
                      </div>

                      <div className="match-details">
                        <div className="score-box">
                          <span>Status</span>
                          <strong>{application.status}</strong>
                        </div>

                        <div className="score-box">
                          <span>Application Date</span>
                          <strong>{application.application_date || "Not set"}</strong>
                        </div>

                        <div className="score-box">
                          <span>Deadline</span>
                          <strong>{application.deadline || "Not set"}</strong>
                        </div>

                        <div className="score-box">
                          <span>Interview</span>
                          <strong>
  {application.interview_date
    ? application.interview_date
    : "Not scheduled"}
</strong>

{application.interview_status && (
  <small
    style={{
      display: "block",
      marginTop: "5px"
    }}
  >
    {application.interview_status}
  </small>
)}
                        </div>
                      </div>

                      {application.job_description && (
                        <div className="reasoning-section">
                          <h3>Job Description</h3>
                          <p>{application.job_description}</p>
                        </div>
                      )}

                      {application.notes && (
                        <div className="reasoning-section">
                          <h3>Notes / Follow-up</h3>
                          <p>{application.notes}</p>
                        </div>
                      )}

                      <div
                        className="career-actions"
                        style={{
                          marginTop: "20px",
                          paddingTop: "20px",
                          borderTop: "1px solid #e5e7eb",
                          display: "flex",
                          gap: "12px",
                          alignItems: "center",
                          flexWrap: "wrap"
                        }}
                      >
                        <input
  type="date"
  value={application.interview_date || ""}
  onChange={(e) =>
    updateApplication(application.id, {
      interview_date: e.target.value
    })
  }
  style={{
    padding: "10px",
    borderRadius: "8px",
    border: "1px solid #d1d5db"
  }}
/>
                        <select
                          value={application.status}
                          onChange={(e) =>
                            updateApplication(application.id, {
                              status: e.target.value
                            })
                          }
                          style={{
                            padding: "10px",
                            borderRadius: "8px",
                            border: "1px solid #d1d5db"
                          }}
                        >
                          <option value="Saved">Saved</option>
                          <option value="Planning to apply">Planning to apply</option>
                          <option value="Applied">Applied</option>
                          <option value="Application under review">Application under review</option>
                          <option value="Shortlisted">Shortlisted</option>
                          <option value="Interview scheduled">Interview scheduled</option>
                          <option value="Interview completed">Interview completed</option>
                          <option value="Offer received">Offer received</option>
                          <option value="Rejected">Rejected</option>
                          <option value="Withdrawn">Withdrawn</option>
                        </select>

                        <button
                          className="view-btn"
                          onClick={() =>
                            updateApplication(application.id, {
                              interview_status:
                                application.interview_status === "Scheduled"
                                  ? "Completed"
                                  : "Scheduled"
                            })
                          }
                        >
                          {application.interview_status === "Scheduled"
                            ? "✓ Interview Completed"
                            : "📅 Mark Interview Scheduled"}
                        </button>

                        <button
                          className="danger-button"
                          onClick={() => deleteApplication(application.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        );


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
