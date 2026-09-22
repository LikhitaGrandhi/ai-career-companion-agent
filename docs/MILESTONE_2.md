# Milestone 2 — Internship Knowledge Base, RAG & Job-Resume Matching

## 1. Milestone Overview

Milestone 2 focuses on building an internship knowledge base, implementing semantic retrieval using RAG techniques, developing a Job-Resume Matching Agent, and validating the system using sample student profiles.

The completed pipeline is:

Student Profile
↓
Semantic Query Generation
↓
Job Knowledge Base
↓
Embedding Generation
↓
FAISS Vector Search
↓
Relevant Internship Retrieval
↓
Job-Resume Matching Agent
↓
Skill / Education / Experience / Project Comparison
↓
Match Score
↓
Reasoning and Missing Skills
↓
Ranked Internship Recommendations

---

# 2. M2.1 — Internship Knowledge Base

## Objective

Create a structured internship knowledge base containing sample internship job postings.

## Dataset

A development dataset containing 180 sample internship records was created.

The dataset contains the following fields:

- Job ID
- Job Title
- Company
- Location
- Description
- Responsibilities
- Required Skills
- Preferred Skills
- Qualifications
- Experience
- Education

Dataset file:

```text
data/internship_jobs_m2_dataset.csv
# Dataset Statistics

| Property | Value |
|---|---:|
| Raw job records | 180 |
| Records after duplicate removal | 60 |
| Indexed job documents | 60 |

The dataset is a synthetic/development dataset created for system development and evaluation. The company names and internship postings are sample data and should not be interpreted as verified current job openings.

## Data Cleaning

The preprocessing pipeline performs the following steps:

1. Loads the internship dataset from CSV.
2. Removes completely empty rows.
3. Removes duplicate job postings.
4. Handles missing values in text fields.
5. Converts relevant fields into consistent string representations.
6. Combines the job fields into structured searchable documents.

The duplicate removal process uses the following fields:

- Job Title
- Company
- Location
- Description
- Responsibilities

Implementation file:

```text
backend/rag/prepare_jobs.py

---

# 3. M2.2 — RAG Pipeline

## Objective

Implement a semantic retrieval pipeline that converts internship job postings into vector embeddings and retrieves relevant internship opportunities based on a student's query.

The implemented pipeline is:

```text
Job Postings
      ↓
Data Cleaning
      ↓
Job Document Creation
      ↓
Text Embeddings
      ↓
FAISS Vector Index
      ↓
Semantic Search
      ↓
Top-K Relevant Jobs

```

## Embedding Model

The project uses the Sentence Transformers library to generate vector embeddings for internship job documents.

### Model Used

```text
all-MiniLM-L6-v2
```

This model converts each job document into a numerical vector representation that captures the semantic meaning of the job posting.

### Embedding Dimension

```text
384
```

Implementation file:

```text
backend/rag/embeddings.py
```

## Vector Database / Index

FAISS (Facebook AI Similarity Search) is used to store and search the generated job embeddings efficiently.

The project uses:

```text
FAISS IndexFlatIP
```

The embeddings are normalized before indexing. Inner-product similarity is therefore used to measure semantic similarity between the student query and job postings.

Implementation file:

```text
backend/rag/vector_store.py
```

## Vector Store Statistics

The generated vector store contains:

| Property | Value |
|---|---:|
| Indexed job documents | 60 |
| Embedding dimension | 384 |
| Similarity method | Inner Product |
| Vector index | FAISS IndexFlatIP |

Generated files:

```text
data/vector_store/jobs.index
data/vector_store/jobs_metadata.json
```

## Semantic Search

The semantic search module converts a user query into an embedding and searches the FAISS index for the most similar internship postings.

Implementation file:

```text
backend/rag/search_jobs.py
```

### Example Query

```text
Python machine learning internship with data science skills
```

### Example Retrieval Results

| Rank | Internship | Company | Similarity Score |
|---|---|---|---:|
| 1 | Machine Learning Intern - Summer Internship | ApexGrid | 0.7249 |
| 2 | AI/ML Intern - Summer Internship | DataSphere Analytics | 0.7216 |
| 3 | AI/ML Intern - Technology Intern | DataSphere Analytics | 0.7173 |
| 4 | Data Science Intern - Summer Internship | AsterByte Systems | 0.6986 |
| 5 | Machine Learning Intern - Technology Intern | ApexGrid | 0.6966 |

The results demonstrate that the system can retrieve internship postings that are semantically related to the student's requested skills and career domain.

---

# 4. M2.3 — Job-Resume Matching Agent

## Objective

The Job-Resume Matching Agent compares a student's profile with the internship opportunities retrieved from the semantic search system.

The matching process considers:

- Required skills
- Preferred skills
- Educational background
- Experience
- Student projects
- Semantic similarity

Implementation file:

```text
backend/agents/job_resume_matcher.py
```

## Matching Pipeline

```text
Student Profile
       ↓
Student Skills
       ↓
Retrieved Internship Jobs
       ↓
Required Skill Comparison
       ↓
Preferred Skill Comparison
       ↓
Education Comparison
       ↓
Experience Comparison
       ↓
Project Relevance
       ↓
Semantic Similarity
       ↓
Overall Match Score
       ↓
Missing Skills + Reasoning
       ↓
Ranked Jobs
```

## Skill Normalization

The matching agent normalizes common variations of technical skills before comparison.

Examples:

| Input | Normalized Skill |
|---|---|
| ML | Machine Learning |
| AI/ML | Machine Learning |
| sklearn | Scikit-learn |
| JS | JavaScript |
| Node | Node.js |
| NodeJS | Node.js |
| ReactJS | React |
| Postgres | PostgreSQL |

This improves consistency when comparing student skills with internship requirements.

## Match Score Calculation

The current baseline matching system uses the following weighted components:

| Component | Weight |
|---|---:|
| Required Skills | 40% |
| Preferred Skills | 10% |
| Education | 15% |
| Experience | 10% |
| Projects | 10% |
| Semantic Similarity | 15% |
| **Total** | **100%** |

The individual scores are combined using these weights to calculate the overall internship compatibility score.

## Matching Output

For every retrieved internship, the agent generates:

- Overall match score
- Semantic similarity score
- Required skill score
- Preferred skill score
- Education score
- Experience score
- Project score
- Matched required skills
- Missing required skills
- Matched preferred skills
- Explanation/reasoning

### Example Matching Result

```text
Overall Match: 73.43%

Matched Required Skills:
- machine learning
- python
- sql

Missing Required Skills:
- deep learning

Reasoning:
- Matches required skills: machine learning, python, sql
- Missing required skills: deep learning
- Educational background is aligned with the role.
- Student projects show strong relevance to the role.
```

The internship results are sorted according to the calculated overall match score.

---

# 5. M2.4 — Evaluation and Validation

## Objective

The matching system was evaluated using multiple sample student profiles to validate the performance of the retrieval and matching pipeline.

The evaluation checks:

- Semantic retrieval
- Skill matching
- Match score generation
- Missing skill detection
- Reasoning generation

Three sample student profiles were evaluated:

1. AI/Data Science Student
2. Web Development Student
3. Java Backend Student

Implementation file:

```text
backend/evaluation/test_m2_evaluation.py
```

## Profile 1 — AI/Data Science Student

### Query

```text
Python machine learning data science internship
```

The system retrieved relevant Machine Learning, Data Science, and AI/ML internship roles.

### Top Job Analysis

```text
Matched Skills:
- machine learning
- numpy
- pandas
- python

Missing Skills:
- scikit-learn
```

## Profile 2 — Web Development Student

### Query

```text
React JavaScript web development internship
```

The system retrieved relevant Full Stack Development and Product Engineering internship roles.

### Top Job Analysis

```text
Matched Skills:
- javascript
- mongodb
- node.js
- react

Missing Skills:
- git
```

## Profile 3 — Java Backend Student

### Query

```text
Java backend software development internship
```

The system retrieved relevant Backend Development and Mobile App Development internship roles.

### Top Job Analysis

```text
Matched Skills:
- java
- sql

Missing Skills:
- git
- python
- rest apis

Preferred Skill Match:
- spring boot
```

---

# 6. M2.4 Evaluation Results

The final evaluation produced the following results:

| Metric | Result |
|---|---:|
| Profiles evaluated | 3 |
| Retrieval pass rate | 100.00% |
| Skill matching success | 100.00% |
| Reasoning generation success | 100.00% |
| Average match score | 63.47% |
| Match score range | 23.89 |

## Retrieval Relevance by Profile

| Profile | Retrieval Relevance |
|---|---:|
| AI/Data Science Student | 100.00% |
| Web Development Student | 66.67% |
| Java Backend Student | 66.67% |

The evaluation considers a profile to have passed retrieval validation when at least 50% of the expected keywords are represented in the retrieved job content.

All three test profiles passed this threshold:

```text
Retrieval Pass Rate = 3 / 3 × 100
                    = 100%
```

The retrieval pass rate should not be confused with the average retrieval relevance across all profiles.

---

# 7. Technology Stack

## Programming Language

- Python 3.12

## NLP / Machine Learning

- Sentence Transformers
- all-MiniLM-L6-v2

## Vector Search

- FAISS
- NumPy

## Data Processing

- Pandas

## Backend

- FastAPI
- MongoDB
- PyMongo

## Development Tools

- Visual Studio Code
- Git
- GitHub

---

# 8. Project Structure

```text
ai-career-companion-agent/
│
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── job_resume_matcher.py
│   │   └── test_matcher.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── mongodb.py
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── test_m2_evaluation.py
│   │
│   ├── models/
│   │   └── student.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── prepare_jobs.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── search_jobs.py
│   │
│   ├── services/
│   │   ├── resume_parser.py
│   │   └── resume_extractor.py
│   │
│   └── main.py
│
├── data/
│   ├── internship_jobs_m2_dataset.csv
│   └── vector_store/
│       ├── jobs.index
│       └── jobs_metadata.json
│
└── docs/
    ├── MILESTONE_1.md
    └── MILESTONE_2.md
```

---

# 9. M2 System Architecture

```text
                    ┌──────────────────────────┐
                    │ Internship Job Dataset   │
                    │ 180 Raw Records          │
                    └────────────┬─────────────┘
                                 ↓
                    ┌──────────────────────────┐
                    │ Data Cleaning             │
                    │ Duplicate Removal        │
                    │ Missing Value Handling   │
                    └────────────┬─────────────┘
                                 ↓
                    ┌──────────────────────────┐
                    │ 60 Unique Job Documents  │
                    └────────────┬─────────────┘
                                 ↓
                    ┌──────────────────────────┐
                    │ Sentence Transformer     │
                    │ all-MiniLM-L6-v2         │
                    └────────────┬─────────────┘
                                 ↓
                    ┌──────────────────────────┐
                    │ 384-Dimensional          │
                    │ Job Embeddings           │
                    └────────────┬─────────────┘
                                 ↓
                    ┌──────────────────────────┐
                    │ FAISS Vector Index       │
                    │ IndexFlatIP              │
                    └────────────┬─────────────┘
                                 ↑
                                 │
              ┌──────────────────┴──────────────────┐
              │                                     │
              │                                     │
    ┌─────────┴──────────┐               ┌─────────┴──────────┐
    │ Student Profile    │               │ Search Query       │
    │ Skills             │               │ Career Interest    │
    │ Education          │               │ Desired Skills     │
    │ Experience         │               └─────────┬──────────┘
    │ Projects           │                         │
    └─────────┬──────────┘                         │
              │                                    │
              └────────────────┬───────────────────┘
                               ↓
                    ┌──────────────────────────┐
                    │ Semantic Job Retrieval   │
                    │ Top-K Relevant Jobs      │
                    └────────────┬─────────────┘
                                 ↓
                    ┌──────────────────────────┐
                    │ Job-Resume Matching      │
                    │ Agent                    │
                    └────────────┬─────────────┘
                                 ↓
             ┌───────────────────┼───────────────────┐
             ↓                   ↓                   ↓
      Skill Matching      Education Match     Experience Match
             │                   │                   │
             └───────────────────┼───────────────────┘
                                 ↓
                    ┌──────────────────────────┐
                    │ Project Relevance +      │
                    │ Semantic Similarity      │
                    └────────────┬─────────────┘
                                 ↓
                    ┌──────────────────────────┐
                    │ Overall Match Score      │
                    └────────────┬─────────────┘
                                 ↓
              ┌──────────────────┼──────────────────┐
              ↓                  ↓                  ↓
       Matched Skills      Missing Skills      Reasoning
              └──────────────────┼──────────────────┘
                                 ↓
                    ┌──────────────────────────┐
                    │ Ranked Internship        │
                    │ Recommendations          │
                    └──────────────────────────┘
```

---

# 10. Limitations and Future Improvements

The current M2 implementation is a baseline matching system developed for internship project evaluation.

## Current Limitations

1. The dataset contains 180 raw records and 60 unique records after duplicate removal.
2. The dataset is synthetic/development data and does not represent verified live internship openings.
3. The current embedding implementation represents each complete job posting as one document rather than indexing individual sections separately.
4. Skill, education, experience, and project matching currently use deterministic rule-based logic.
5. The evaluation currently uses three sample student profiles.
6. Retrieval evaluation uses keyword-based relevance as a lightweight validation metric.
7. The current matching agent provides deterministic reasoning rather than LLM-generated explanations.

## Future Improvements

- Expand the unique internship knowledge base.
- Implement section-level job chunking.
- Create a larger labelled evaluation dataset.
- Improve experience and qualification matching.
- Add weighted skill importance.
- Use an LLM for richer matching explanations.
- Connect the matching agent directly to MongoDB student profiles.
- Expose the matching functionality through FastAPI APIs.
- Build a React interface for internship recommendations.
- Integrate verified external internship sources where appropriate.

---

# 11. Milestone 2 Completion

The following M2 requirements have been implemented:

| Requirement | Status |
|---|---|
| Internship knowledge base | ✅ Completed |
| Job data cleaning | ✅ Completed |
| Job document preparation | ✅ Completed |
| Embedding generation | ✅ Completed |
| FAISS vector indexing | ✅ Completed |
| Semantic job retrieval | ✅ Completed |
| Job-Resume Matching Agent | ✅ Completed |
| Required skill matching | ✅ Completed |
| Preferred skill matching | ✅ Completed |
| Education matching | ✅ Completed |
| Experience matching | ✅ Completed |
| Project relevance matching | ✅ Completed |
| Match score calculation | ✅ Completed |
| Missing skill detection | ✅ Completed |
| Matching reasoning | ✅ Completed |
| Retrieval validation | ✅ Completed |
| Skill matching validation | ✅ Completed |
| Reasoning validation | ✅ Completed |

## Final Status

**Milestone 2 — Completed**

The system can retrieve semantically relevant internship opportunities and compare them against student profiles using skills, education, experience, projects, and semantic similarity.

It generates compatibility scores, identifies missing skills, provides matching reasoning, and ranks internship opportunities for further career assistance.