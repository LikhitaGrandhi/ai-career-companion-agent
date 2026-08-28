# AI Career Companion Agent for Internship Matching and Interview Preparation

## Project Overview

The **AI Career Companion Agent** is an AI-powered career assistance system designed to help students with internship applications and career preparation.

The system creates a structured student profile from the student's details and uploaded resume. In future milestones, the system will use this profile to match students with suitable internships, identify skill gaps, generate cover letters, and provide interview preparation.

## Milestone 1 – Foundation & Candidate Understanding

### M1.1 – Research & Technical Understanding

* Studied internship application workflows.
* Studied Retrieval-Augmented Generation (RAG) architecture.
* Studied multi-agent design patterns.
* Identified suitable technologies for the system.

### M1.2 – System Architecture

The system architecture contains:

* Student/User Interface
* Backend/API Layer
* Resume Upload and Storage
* Resume Parsing Module
* LLM
* Candidate Profile Database
* Job-Posting Knowledge Base
* RAG Pipeline
* AI Agent Layer
* Application Tracking Module

### M1.3 – Student Profile Module

The student profile contains:

* Personal information
* Education
* Skills
* Experience
* Projects
* Certifications
* Resume information

The system will support student profile creation and resume upload.

### M1.4 – Resume Parsing & Extraction

The resume processing pipeline is:

Student Resume → Text Extraction → LLM Processing → Structured Candidate Profile

The system extracts:

* Name
* Contact information
* Education
* Skills
* Experience
* Projects
* Certifications

The extraction process will be tested using multiple sample resumes.

## AI Agents

The planned AI agent layer contains:

1. **Resume Agent** – Parses resumes and extracts structured candidate information.
2. **Job-Resume Matching Agent** – Compares candidate profiles with internship requirements.
3. **Skill Gap Agent** – Identifies missing skills required for suitable jobs.
4. **Cover Letter Agent** – Generates customized cover letters.
5. **Interview Agent** – Provides interview questions and preparation.
6. **Career Assistant** – Provides general career guidance.

## System Architecture

```text
                         STUDENT
                            |
                            v
                  +-------------------+
                  | Student Interface |
                  | Profile & Resume  |
                  | Upload            |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  |   Backend / API   |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  | Resume Processing |
                  | & Text Extraction |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  |       LLM         |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  | Candidate Profile |
                  |     Database      |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  |    AI Agents      |
                  +-------------------+
                    /   /   |   \   \
                   /   /    |    \   \
              Resume Match Skill Cover Interview
              Agent  Agent  Gap  Letter Agent
                                      |
                                      v
                              Career Assistant
```

## Technology Stack

| Component         | Technology                   |
| ----------------- | ---------------------------- |
| Frontend          | React.js                     |
| Backend           | Python, FastAPI              |
| Database          | MongoDB                      |
| AI/LLM            | LLM API                      |
| Resume Processing | Python                       |
| RAG               | Embeddings + Vector Database |
| API Testing       | Postman                      |
| Version Control   | Git, GitHub                  |

## Project Structure

```text
ai-career-companion-agent/
│
├── README.md
│
├── docs/
│   ├── research.md
│   ├── architecture.md
│   └── candidate-profile.md
│
├── backend/
├── frontend/
│
└── resume_samples/
```

## Future Scope

Future milestones will extend the system with:

* Internship/job recommendation
* RAG-based job search
* Skill gap analysis
* Cover letter generation
* Interview preparation
* Application tracking
* Career assistance
* Multi-agent orchestration
