# M1.2 – System Architecture

## System Overview

The AI Career Companion consists of a user interface, backend API, resume processing module, LLM, database, RAG pipeline, and AI agent layer.

## Architecture Diagram

```text
                         STUDENT
                            |
                            v
                 +--------------------+
                 |  Student Interface |
                 |                    |
                 | Profile Creation   |
                 | Resume Upload      |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 |   Backend / API    |
                 |      FastAPI       |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 | Resume Processing  |
                 |  Text Extraction   |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 |       LLM          |
                 | Information        |
                 | Extraction          |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 | Candidate Profile  |
                 |      MongoDB       |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 |    AI Agent Layer  |
                 +--------------------+
                   /    /   |    \    \
                  /    /    |     \    \
               Resume Match Skill Cover Interview
               Agent  Agent  Gap  Letter Agent
                                      |
                                      v
                              Career Assistant
```

## Major Components

### 1. Student/User Interface

Allows students to:

* Create their profile.
* Enter educational information.
* Enter skills and experience.
* Upload resumes.

### 2. Backend/API Layer

FastAPI provides APIs for:

* Student profile creation.
* Resume upload.
* Resume processing.
* Candidate profile management.

### 3. Resume Processing Module

The module extracts text from uploaded resumes and sends the extracted information for structured processing.

### 4. LLM

The LLM processes resume text and extracts structured information such as skills, education, experience, and projects.

### 5. Candidate Profile Database

MongoDB stores structured candidate information and resume metadata.

### 6. Job Knowledge Base

Job and internship postings will be stored and indexed for future retrieval.

### 7. RAG Pipeline

The RAG pipeline will retrieve relevant internship information from the job knowledge base and provide it to the LLM.

### 8. AI Agent Layer

The planned agents are:

* Resume Agent
* Job-Resume Matching Agent
* Skill Gap Agent
* Cover Letter Agent
* Interview Agent
* Career Assistant

## Data Flow

```text
Resume Upload
     ↓
Resume Storage
     ↓
Text Extraction
     ↓
LLM Processing
     ↓
Structured Candidate Data
     ↓
Candidate Profile
     ↓
AI Agents
```

The architecture can be extended in future milestones as additional functionality is implemented.
