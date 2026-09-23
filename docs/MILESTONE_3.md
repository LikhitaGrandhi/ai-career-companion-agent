# Milestone 3 — Career Intelligence Agents

## 1. Overview

Milestone 3 focuses on building career-support agents that help students prepare for internships after identifying suitable opportunities.

The implemented agents provide:

- Skill gap analysis
- Resume customization
- Cover letter generation
- Interview preparation
- Conversational career assistance

The agents operate on structured student-profile and internship-job data produced by the earlier milestones.

---

## 2. Milestone 3 Objectives

The objectives of M3 are:

1. Develop a Skill Gap Analysis Agent.
2. Develop a Resume and Cover Letter Customization Agent.
3. Develop an Interview Preparation Agent.
4. Develop a Conversational Career Assistant.
5. Integrate the agents using a common student profile and selected internship role.
6. Evaluate each agent using representative test cases.

---

# 3. M3.1 — Skill Gap Analysis Agent

## 3.1 Purpose

The Skill Gap Agent compares the student's existing skills with the required and preferred skills of a selected internship.

It identifies:

- Matched required skills
- Missing required skills
- Matched preferred skills
- Missing preferred skills
- Required-skill match percentage
- Preferred-skill match percentage
- Critical skill gaps
- Learning recommendations

## 3.2 Implementation

File:

`backend/agents/skill_gap_agent.py`

The agent normalizes skill names using aliases such as:

~~~text
ml → machine learning
ai/ml → machine learning
sklearn → scikit-learn
scikit learn → scikit-learn
js → javascript
node → node.js
nodejs → node.js
reactjs → react
postgres → postgresql
~~~

The normalized student skills are compared against the job's required and preferred skills.

## 3.3 Example

Student skills:

~~~text
Python
Machine Learning
Pandas
SQL
~~~

Required skills:

~~~text
Python
NumPy
Pandas
Scikit-learn
Machine Learning
~~~

Result:

~~~text
Matched required:
Python
Pandas
Machine Learning

Missing required:
NumPy
Scikit-learn
~~~

The system also generates recommendations for missing skills.

## 3.4 Evaluation

Three student profiles were evaluated:

1. Partial Machine Learning Skills
2. Strong Machine Learning Skills
3. Different Technical Background

The evaluation successfully produced skill-gap results and learning recommendations for all three profiles.

---

# 4. M3.2 — Resume and Cover Letter Customization Agent

## 4.1 Purpose

The Resume and Cover Letter Agent creates a role-specific resume draft and cover letter using information already available in the student's profile.

A key requirement is to avoid inventing skills, achievements, experience, or qualifications.

## 4.2 Implementation

File:

`backend/agents/resume_customization_agent.py`

The agent:

1. Reads the student's profile.
2. Reads the selected internship.
3. Identifies relevant student skills.
4. Creates a customized resume structure.
5. Generates a role-specific professional summary.
6. Generates a cover letter.

## 4.3 Resume Sections

The generated resume structure contains:

~~~text
Candidate Name
Target Role
Company
Professional Summary
Relevant Skills
Education
Experience
Projects
~~~

## 4.4 Cover Letter

The cover letter includes:

- Internship role
- Company
- Relevant student skills
- Interest in the opportunity
- Learning and contribution statement
- Candidate name

The system uses only information supplied in the student profile.

## 4.5 Evaluation

Evaluation file:

`backend/evaluation/test_resume_customization.py`

Results:

~~~text
Resume sections present: True
No invented skills: True
Cover letter generated: True

Overall M3.2 Result: PASS
~~~

---

# 5. M3.3 — Interview Preparation Agent

## 5.1 Purpose

The Interview Preparation Agent creates a structured preparation plan for a selected internship.

It generates questions from:

- Student technical skills
- Student projects
- Internship role
- General HR topics

## 5.2 Implementation

File:

`backend/agents/interview_agent.py`

The agent produces four categories of questions.

### Technical Questions

Questions based on the student's actual skills.

Example:

~~~text
Explain your understanding of Python and how you have used it.
~~~

### Project Questions

Questions based on projects listed by the student.

Example:

~~~text
Explain the AI Resume Analyzer project.
What problem did it solve?
~~~

### Role Questions

Questions related to the selected internship.

Example:

~~~text
Why are you interested in the Machine Learning Intern role?
~~~

### HR Questions

General behavioral questions such as:

~~~text
Tell me about yourself.

What are your strengths?

Describe a technical challenge you faced and how you handled it.
~~~

## 5.3 Preparation Tips

The agent also provides preparation guidance, including:

- Review required skills.
- Prepare to explain every project.
- Revise internship-related fundamentals.
- Prepare examples of technical problems solved.
- Practice clear and concise communication.

## 5.4 Evaluation

Evaluation file:

`backend/evaluation/test_interview_agent.py`

Results:

~~~text
Sections present: True
Technical questions generated: True
Project questions generated: True
Role questions generated: True
HR questions generated: True
Preparation tips generated: True
Student skills referenced: True
Student projects referenced: True

Overall M3.3 Result: PASS
~~~

---

# 6. M3.4 — Conversational Career Assistant

## 6.1 Purpose

The Conversational Career Assistant provides a single interface for accessing the career-support agents.

Instead of directly interacting with individual agents, the user can ask a natural-language career question.

The assistant identifies the request and routes it to the appropriate functionality.

## 6.2 Implementation

File:

`backend/agents/career_assistant.py`

The assistant currently supports the following intents:

~~~text
skill_gap
resume
cover_letter
interview
job_information
general
~~~

## 6.3 Agent Integration

The Career Assistant integrates the following components:

~~~text
                    Career Assistant
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
    Skill Gap Agent   Resume Agent    Interview Agent
          |                |
          v                v
     Gap Analysis     Resume/Cover Letter
~~~

It also provides selected internship information when requested.

## 6.4 Example Queries

### Skill Gap

~~~text
What skills am I missing?
~~~

Output:

~~~text
Intent: skill_gap
~~~

### Resume

~~~text
Help me customize my resume
~~~

Output:

~~~text
Intent: resume
~~~

### Cover Letter

~~~text
Write a cover letter
~~~

Output:

~~~text
Intent: cover_letter
~~~

### Interview

~~~text
Prepare me for the interview
~~~

Output:

~~~text
Intent: interview
~~~

### Internship Information

~~~text
Tell me about this internship
~~~

Output:

~~~text
Intent: job_information
~~~

### General

~~~text
What can you help me with?
~~~

Output:

~~~text
Intent: general
~~~

---

# 7. M3.4 Evaluation

Evaluation file:

`backend/evaluation/test_career_assistant.py`

Six representative queries were tested.

| Query Type | Expected Intent | Result |
|---|---|---|
| Skill Gap | skill_gap | PASS |
| Resume | resume | PASS |
| Cover Letter | cover_letter | PASS |
| Interview | interview | PASS |
| Job Information | job_information | PASS |
| General | general | PASS |

Evaluation results:

~~~text
Passed Tests: 6
Total Tests: 6
Intent Accuracy: 100.0%

Overall M3.4 Result: PASS
~~~

---

# 8. Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn
- MongoDB
- Pandas

## Machine Learning / NLP

- Sentence Transformers
- FAISS
- Rule-based skill normalization
- Semantic similarity

## Career Agents

- Skill Gap Agent
- Resume Customization Agent
- Interview Preparation Agent
- Conversational Career Assistant

---

# 9. Project Structure

The M3-related structure is:

~~~text
backend/
├── agents/
│   ├── __init__.py
│   ├── job_resume_matcher.py
│   ├── skill_gap_agent.py
│   ├── resume_customization_agent.py
│   ├── interview_agent.py
│   ├── career_assistant.py
│   └── test_matcher.py
│
└── evaluation/
    ├── __init__.py
    ├── test_m2_evaluation.py
    ├── test_skill_gap.py
    ├── test_resume_customization.py
    ├── test_interview_agent.py
    └── test_career_assistant.py
~~~

---

# 10. Agent Data Flow

The overall M3 workflow is:

~~~text
Student Profile
       |
       v
Selected Internship
       |
       v
Career Assistant
       |
       +--------------------+
       |                    |
       v                    v
 Skill Gap             Resume Agent
       |                    |
       v                    +------> Customized Resume
 Skill Recommendations     |
                            +------> Cover Letter
       |
       +--------------------+
       |
       v
Interview Agent
       |
       +------> Technical Questions
       |
       +------> Project Questions
       |
       +------> Role Questions
       |
       +------> HR Questions
~~~

---

# 11. Safety and Data Integrity

The system follows several important constraints:

- Resume customization uses information from the student's profile.
- The system does not intentionally add skills that are absent from the student's profile.
- Interview project questions are based on projects supplied by the student.
- Skill-gap analysis distinguishes matched and missing skills.
- Career Assistant responses are routed using explicit intent rules.
- The current implementation does not claim to use an LLM for agent generation.

---

# 12. Evaluation Summary

| Component | Evaluation | Result |
|---|---|---|
| Skill Gap Agent | 3 student profiles | PASS |
| Resume Customization | Sections + skill integrity + cover letter | PASS |
| Interview Agent | Question categories + student references | PASS |
| Career Assistant | 6 intent tests | 100% accuracy |

---

# 13. Current Limitations

The current M3 implementation is a functional baseline.

### Skill Gap Agent

Currently focuses primarily on skill comparison. More advanced versions can also classify:

- Critical gaps
- Partial skills
- Experience gaps
- Qualification gaps
- Education gaps

### Resume Customization

The current implementation creates a structured customized resume draft. Future versions can use an LLM for richer language generation while maintaining strict grounding in the student's profile.

### Interview Agent

The current implementation generates preparation questions but does not yet conduct a complete interactive mock interview or evaluate the student's answers.

### Career Assistant

The current assistant uses rule-based intent routing. Future versions can use an LLM-based conversational layer and integrate RAG retrieval for richer career-related responses.

---

# 14. Future Improvements

Planned improvements include:

1. LLM-powered response generation.
2. Interactive mock interviews.
3. Answer evaluation and feedback.
4. More detailed skill-gap classification.
5. RAG-based career knowledge retrieval.
6. Persistent conversation context.
7. Better personalization using the complete student profile.
8. React-based web interface.
9. Backend API integration with the frontend.
10. Deployment of the complete application.

---

# 15. Milestone 3 Completion

Milestone 3 successfully implements the four planned career-support components:

~~~text
M3.1 Skill Gap Agent              ✅
M3.2 Resume & Cover Letter Agent  ✅
M3.3 Interview Preparation Agent  ✅
M3.4 Conversational Assistant     ✅
~~~

The M3 components have been individually tested and integrated into a common career-support workflow.

**Milestone 3 Status: COMPLETE**