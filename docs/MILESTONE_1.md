# Milestone 1 — AI Career Companion Agent

## 1. Project Overview

The AI Career Companion Agent is an AI-powered career assistance system designed to help students with internship discovery, resume analysis, skill-gap identification, interview preparation, and career guidance.

The system uses a FastAPI backend, MongoDB database, resume parsing and extraction services, and a modular multi-agent architecture.

---

# 2. M1.1 — Research & Technical Understanding

## 2.1 Internship Workflow

The proposed internship assistance workflow is:

Student
↓
Create Profile / Upload Resume
↓
Resume Parsing
↓
Resume Information Extraction
↓
Student Profile Storage
↓
Internship / Job Collection
↓
Job-Resume Matching
↓
Skill Gap Analysis
↓
Resume Improvement
↓
Cover Letter Generation
↓
Interview Preparation
↓
Career Assistance

---

## 2.2 RAG Architecture

Retrieval-Augmented Generation (RAG) combines information retrieval with a language model.

The system first retrieves relevant information from a knowledge source and then provides that information to an AI model to generate a useful response.

Future RAG pipeline:

Student Query
↓
Query Processing
↓
Knowledge Base / Job Data / Career Resources
↓
Relevant Information Retrieval
↓
Context Construction
↓
AI Model
↓
Personalized Response

RAG can be used in the Career Assistant to provide responses based on internship information, job descriptions, career resources, and student profile information.

---

## 2.3 Multi-Agent Architecture

The system is designed as a modular multi-agent system.

Each agent is responsible for a specific career-related task.

The planned agents are:

1. Job-Resume Matching Agent
2. Skill Gap Agent
3. Resume Agent
4. Cover Letter Agent
5. Interview Agent
6. Career Assistant

A central system can coordinate these agents based on the student's request.

---

# 3. M1.2 — System Architecture

## 3.1 High-Level Architecture

```text
                         STUDENT
                            |
                            v
                    +---------------+
                    |    Frontend   |
                    | React / Web UI|
                    +---------------+
                            |
                            v
                    +---------------+
                    | FastAPI       |
                    | Backend       |
                    +---------------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
      Student Profile   Resume Module   Future APIs
             |              |
             |              v
             |       +--------------+
             |       | PDF Parser   |
             |       +--------------+
             |              |
             |              v
             |       +--------------+
             |       | Resume       |
             |       | Extractor    |
             |       +--------------+
             |              |
             +--------------+
                            |
                            v
                    +---------------+
                    |   MongoDB     |
                    |   Database     |
                    +---------------+
                            |
                            v
                  Future AI Agent Layer
                            |
        +---------+---------+---------+---------+
        |         |         |         |         |
        v         v         v         v         v
      Job      Skill     Resume    Cover     Interview
    Matching    Gap       Agent    Letter      Agent
      Agent    Agent               Agent
                            |
                            v
                    Career Assistant

# 4. Agent Responsibilities

## 4.1 Job-Resume Matching Agent

- Compares student resume information with internship/job requirements.
- Identifies matching skills.
- Identifies missing requirements.
- Produces a job-resume compatibility result.

## 4.2 Skill Gap Agent

- Compares existing student skills with required skills.
- Identifies missing technical skills.
- Recommends technologies and learning resources.
- Generates a personalized learning roadmap.

## 4.3 Resume Agent

- Analyzes the student's resume.
- Identifies areas for improvement.
- Suggests better project descriptions.
- Provides ATS-friendly resume recommendations.

## 4.4 Cover Letter Agent

- Generates personalized cover letters.
- Uses student profile information.
- Uses internship/job description information.
- Customizes the letter for each application.

## 4.5 Interview Agent

- Generates technical interview questions.
- Generates HR questions.
- Creates questions based on the student's skills.
- Provides interview practice and sample answers.

## 4.6 Career Assistant

- Acts as the main conversational career assistant.
- Understands student career-related queries.
- Coordinates the appropriate specialized agents.
- Provides personalized career guidance.

---

# 5. Student Profile Schema

The student profile stores the following information:

```json
{
  "name": "Student Name",
  "email": "student@email.com",
  "phone": "Phone Number",
  "education": [],
  "college": "College Name",
  "branch": "AI & Data Science",
  "cgpa": 9.72,
  "skills": [],
  "projects": [],
  "experience": [],
  "certifications": [],
  "resume_filename": "resume.pdf"
}
---

# 6. M1.3 — Student Profile Module

The Student Profile Module stores structured information about the student.

The profile includes:

- Name
- Email
- Phone
- Education
- College
- Branch
- CGPA
- Skills
- Projects
- Experience
- Certifications
- Resume filename

The backend provides APIs to retrieve student profiles from MongoDB.

### Student Profile Flow

Student
↓
Profile / Resume Upload
↓
Resume Information Extraction
↓
Structured Student Profile
↓
MongoDB
↓
GET /students

---

# 7. M1.4 — Resume Parsing & Extraction

The system provides functionality to upload and process student resumes in PDF format.

### Resume Processing Flow

PDF Resume
↓
POST /resume/upload
↓
PDF File Storage
↓
PDF Text Extraction
↓
Resume Information Extraction
↓
Structured Resume Data
↓
MongoDB
↓
Student Profile

The system extracts the following information:

- Name
- Email
- Phone
- Skills
- Education
- Experience
- Projects
- Certifications

---

# 8. Backend Implementation

The backend is implemented using FastAPI.

### Current API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Checks whether the backend is running |
| GET | `/health` | Checks backend health |
| GET | `/students` | Retrieves student profiles |
| POST | `/resume/upload` | Uploads, parses and saves a resume |

---

# 9. Resume Processing Components

### PDF Parser

The PDF parser extracts raw text from the uploaded resume.

File:

`services/resume_parser.py`

### Resume Extractor

The resume extractor converts the raw resume text into structured information.

File:

`services/resume_extractor.py`

Extracted information includes:

```text
Name
Email
Phone
Skills
Education
Experience
Projects
Certifications

---

# 10. Database Implementation

MongoDB Atlas is used as the database for storing student profile information.

The database stores structured information extracted from uploaded resumes.

### Student Collection

The `students` collection contains fields such as:

```text
_id
name
email
phone
education
college
branch
cgpa
skills
projects
experience
certifications
resume_filename

The FastAPI backend uses PyMongo to communicate with MongoDB Atlas.

When a resume is successfully processed, the extracted student information is stored as a document in the students collection.

---

# 11. API Testing

The backend APIs were tested using FastAPI Swagger UI.

Swagger documentation is available at:

http://127.0.0.1:8000/docs

## 11.1 Root Endpoint

GET /

This endpoint checks whether the backend server is running.

## 11.2 Health Check

GET /health

Example response:

{
  "status": "healthy"
}

The health-check endpoint was successfully tested.

## 11.3 Student Retrieval

GET /students

This endpoint retrieves student profiles stored in MongoDB.

The endpoint was successfully tested and returned the extracted student information stored in the database.

## 11.4 Resume Upload

POST /resume/upload

This endpoint was tested using a student resume in PDF format.

The API successfully:

1. Accepts the PDF resume.
2. Saves the uploaded resume.
3. Extracts text from the PDF.
4. Extracts structured resume information.
5. Stores the extracted information in MongoDB.
6. Returns the extracted student information.

---

# 12. Technology Stack

## Frontend

- React
- HTML
- CSS
- JavaScript

## Backend

- Python
- FastAPI
- Uvicorn

## Database

- MongoDB Atlas
- PyMongo

## Resume Processing

- Python
- PDF parsing
- Resume information extraction

## AI Architecture

- Large Language Model
- Retrieval-Augmented Generation (RAG)
- Multi-Agent Architecture

## Development Tools

- Visual Studio Code
- GitHub
- MongoDB Atlas
- FastAPI Swagger UI

---

# 13. Project Directory Structure

```text
backend/
├── main.py
├── database/
│   ├── __init__.py
│   └── mongodb.py
├── models/
│   ├── __init__.py
│   └── student.py
├── services/
│   ├── resume_parser.py
│   └── resume_extractor.py
├── uploads/
├── .env
└── requirements.txt

# 14. Milestone 1 Testing Results

| Component | Status |
|---|---|
| FastAPI server | Successful |
| MongoDB Atlas connection | Successful |
| GET / | Successful |
| GET /health | Successful |
| GET /students | Successful |
| POST /resume/upload | Successful |
| PDF upload | Successful |
| PDF text extraction | Successful |
| Resume information extraction | Successful |
| MongoDB data storage | Successful |
| MongoDB data retrieval | Successful |
| Swagger API testing | Successful |

# 15. Milestone 1 Completion Status

## M1.1 - Research & Technical Understanding

- Internship application workflow - Completed
- RAG architecture - Completed
- Multi-agent architecture - Completed
- Technology selection - Completed

## M1.2 - System Architecture

- System architecture - Completed
- Agent responsibilities - Completed
- Student profile schema - Completed
- Resume processing flow - Completed
- Data flow - Completed

## M1.3 - Student Profile Module

- Student profile structure - Completed
- MongoDB integration - Completed
- Student profile retrieval - Completed
- Resume upload integration - Completed

## M1.4 - Resume Parsing & Extraction

- PDF resume upload - Completed
- PDF text extraction - Completed
- Structured resume extraction - Completed
- Resume data storage - Completed
- Resume data retrieval - Completed

### Overall Status

Milestone 1 - Completed

# 16. Milestone 1 Outcome

Milestone 1 establishes the foundation of the AI Career Companion Agent.

The system can currently:

1. Accept student resumes in PDF format.
2. Extract text from uploaded resumes.
3. Extract structured student information.
4. Create a structured student profile.
5. Store student information in MongoDB Atlas.
6. Retrieve student profiles through REST APIs.
7. Provide a FastAPI backend for future AI services.

The implemented system provides the basic foundation required for the upcoming RAG pipeline and AI agent components.

The completed Milestone 1 pipeline is:

Student Resume
      |
      v
PDF Upload
      |
      v
PDF Text Extraction
      |
      v
Resume Information Extraction
      |
      v
Structured Student Profile
      |
      v
MongoDB Atlas
      |
      v
Student Profile API

# 17. Future Development - Milestone 2

The next milestone will focus on building the internship knowledge base and Job-Resume Matching Agent.

The planned components are:

- 150-200 sample internship/job postings
- Standard job-posting schema
- Job data cleaning
- Duplicate removal
- Incomplete data handling
- Internship knowledge base
- Job-posting chunking
- Embedding generation
- Vector database/index
- Semantic search
- RAG pipeline
- Job-Resume Matching Agent
- Student-job compatibility scoring
- Matching reasoning
- Top-K job retrieval
- Retrieval evaluation
- Matching accuracy evaluation

# 18. Conclusion

Milestone 1 successfully establishes the backend foundation required for the AI Career Companion Agent.

The system currently provides a working pipeline for:

- Student resume upload
- PDF text extraction
- Resume information extraction
- Student profile creation
- MongoDB Atlas storage
- Student profile retrieval
- FastAPI REST APIs

The overall implemented workflow is:

Student Resume
      |
      v
PDF Upload
      |
      v
PDF Text Extraction
      |
      v
Resume Information Extraction
      |
      v
Structured Student Profile
      |
      v
MongoDB Atlas
      |
      v
Student Profile API

This foundation will be extended in the upcoming milestones to implement internship matching, RAG-based job retrieval, skill-gap analysis, personalized resume and cover-letter generation, interview preparation, and conversational career assistance.

Milestone 1 is completed successfully.