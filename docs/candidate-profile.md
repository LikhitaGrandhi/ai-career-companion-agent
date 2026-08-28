# M1.2 – Candidate Profile Schema

## Candidate Profile

The candidate profile stores structured information about a student.

### Profile Fields

| Field          | Description                                 |
| -------------- | ------------------------------------------- |
| Candidate ID   | Unique identifier                           |
| Name           | Student's full name                         |
| Email          | Student email                               |
| Phone          | Contact number                              |
| Education      | Degree, branch, college and graduation year |
| Skills         | Technical and soft skills                   |
| Experience     | Previous internships or work experience     |
| Projects       | Academic and personal projects              |
| Certifications | Completed certifications                    |
| Resume         | Uploaded resume information                 |

## Example Candidate Profile

```json
{
  "candidate_id": "C001",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "education": [
    {
      "degree": "B.Tech",
      "branch": "Computer Science",
      "college": "ABC University",
      "graduation_year": 2027
    }
  ],
  "skills": [
    "Python",
    "Java",
    "SQL",
    "Machine Learning"
  ],
  "experience": [
    {
      "company": "XYZ Technologies",
      "role": "Software Intern",
      "duration": "3 months"
    }
  ],
  "projects": [
    {
      "name": "AI Chatbot",
      "description": "An AI-based chatbot project"
    }
  ],
  "certifications": [],
  "resume": {
    "filename": "john_doe_resume.pdf",
    "status": "uploaded"
  }
}
```

## Resume-to-Profile Data Flow

```text
Uploaded Resume
      ↓
Text Extraction
      ↓
LLM
      ↓
Structured JSON
      ↓
Candidate Profile
      ↓
Database
```

The structured profile will later be used by the job matching, skill gap, cover letter, interview, and career assistant agents.
