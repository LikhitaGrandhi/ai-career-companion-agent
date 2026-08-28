# M1.1 – Research & Technical Understanding

## 1. Internship Application Workflow

The typical internship application workflow consists of the following steps:

1. Student creates a profile.
2. Student uploads their resume.
3. Internship opportunities are collected from job sources.
4. The student's skills and qualifications are compared with internship requirements.
5. Suitable internships are recommended.
6. The student applies for the selected internship.
7. The system can provide cover letter and interview preparation support.

## 2. RAG Architecture

RAG stands for **Retrieval-Augmented Generation**.

RAG combines information retrieval with a Large Language Model (LLM). Relevant information is first retrieved from a knowledge base and then provided to the LLM to generate a useful response.

### RAG Flow

```text
User Query
    ↓
Retriever
    ↓
Relevant Job Information
    ↓
LLM
    ↓
Generated Response
```

In this project, RAG can be used to retrieve relevant internship and job-posting information before generating recommendations.

## 3. Multi-Agent Design

A multi-agent system uses multiple specialized AI agents. Each agent performs a specific task instead of using one AI system for every task.

The planned agents are:

* **Resume Agent** – Parses resumes and extracts candidate information.
* **Job-Resume Matching Agent** – Matches candidates with suitable internships.
* **Skill Gap Agent** – Identifies missing skills.
* **Cover Letter Agent** – Generates customized cover letters.
* **Interview Agent** – Helps students prepare for interviews.
* **Career Assistant** – Provides general career guidance.

## 4. Technology Selection

The initial technology stack consists of:

* React.js for the user interface.
* Python and FastAPI for backend APIs.
* MongoDB for candidate profile storage.
* LLM API for intelligent resume extraction and career assistance.
* Embeddings and a vector database for future RAG implementation.
* GitHub for version control.

## Conclusion

The research establishes the foundation for developing an AI-powered career companion that can understand student profiles, process resumes, match internships, identify skill gaps, and support interview preparation.
