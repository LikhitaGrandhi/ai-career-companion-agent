# Agile Documentation — AI Career Companion Agent

## 1. Project Overview

**Project Name:** AI Career Companion Agent for Internship Matching and Interview Preparation

**Technology Stack:**
- Frontend: React and Vite
- Backend: Python and FastAPI
- Database: MongoDB Atlas
- Retrieval-Augmented Generation (RAG): Sentence Transformers and FAISS

## 2. Agile Methodology

The project was developed using an iterative, milestone-based approach inspired by Agile principles. The system was divided into smaller modules, implemented incrementally, tested, and integrated into the complete application.

This approach helped us identify issues early, improve existing functionality, and track progress throughout development.

## 3. Milestone Planning

### Milestone 1 — Student Profile and Resume Processing
- Research requirements and system architecture.
- Define the student profile schema.
- Implement student profile management.
- Develop resume upload, parsing, and information extraction.

**Deliverable:** Student profile and resume processing functionality.

### Milestone 2 — Internship Retrieval and Matching
- Prepare the internship dataset.
- Implement text embeddings and FAISS-based vector search.
- Develop the RAG job retrieval pipeline.
- Evaluate internship retrieval and matching results.

**Deliverable:** Internship retrieval and job-matching functionality.

### Milestone 3 — Career Assistance Agents
- Implement skill gap analysis.
- Develop resume customization and cover letter generation.
- Implement interview preparation.
- Integrate the AI Career Assistant.

**Deliverable:** Integrated career assistance features.

### Milestone 4 — Testing, Optimization, and Final Integration
- Develop the Application Tracking module.
- Perform end-to-end testing.
- Optimize job retrieval and skill normalization.
- Prepare technical documentation and the final demonstration.

**Deliverable:** An integrated, tested, and documented AI Career Companion application.

## 4. Task Tracking and Progress

Tasks were organized according to the project milestones. Development included backend APIs, frontend interfaces, database integration, retrieval components, and career assistance agents.

Progress was evaluated by checking whether the planned features were implemented and whether the corresponding workflows operated correctly.

## 5. Testing and Continuous Improvement

Testing was performed throughout development to identify integration issues and verify functionality.

The project testing covered:
- Student profile and resume processing.
- Internship retrieval and job matching.
- Skill gap analysis.
- Resume and cover letter generation.
- Interview preparation and AI Career Assistant.
- Application tracking and MongoDB persistence.
- Frontend and backend integration.

Testing observations were used to improve the retrieval strategy and skill normalization.

## 6. Optimization Results

The job retrieval embedding strategy was refined to focus on job titles, required skills, preferred skills, responsibilities, and qualifications.

For the test query "Python machine learning internship with data science skills", the top-five average semantic similarity increased from **0.7113 to 0.7738**, an improvement of approximately **8.8%**.

This result applies to the specific query tested.

## 7. Final Project Status

The major project modules have been implemented and tested. The application combines student profile management, resume analysis, internship discovery, job matching, skill gap analysis, document generation, interview preparation, career assistance, and application tracking.

The remaining submission activities include verifying the repository documentation, deployment, and final demonstration readiness.
