import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types


# Load environment variables
load_dotenv("backend/.env")


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured in backend/.env")

client = genai.Client(api_key=GEMINI_API_KEY)


# =========================================================
# RESUME EXTRACTION SCHEMA
# =========================================================

class ResumeData(BaseModel):

    name: str = Field(
        description="Candidate's full name. Return an empty string if not present."
    )

    email: str = Field(
        description="Candidate's email address. Return an empty string if not present."
    )

    phone: str = Field(
        description="Candidate's phone number. Return an empty string if not present."
    )

    skills: List[str] = Field(
        description="Technical and professional skills explicitly mentioned in the resume."
    )

    education: List[str] = Field(
        description="Education qualifications explicitly mentioned in the resume."
    )

    experience: List[str] = Field(
        description="Work experience, internships, or professional experience explicitly mentioned."
    )

    projects: List[str] = Field(
        description="Projects explicitly mentioned in the resume."
    )

    certifications: List[str] = Field(
        description="Certifications explicitly mentioned in the resume."
    )


# =========================================================
# GEMINI RESUME EXTRACTION
# =========================================================

def extract_resume_data(text: str):

    if not text or not text.strip():
        return {
            "name": "",
            "email": "",
            "phone": "",
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": []
        }

    prompt = f"""
You are a resume information extraction system.

Extract structured information from the resume text provided below.

IMPORTANT RULES:

1. Extract ONLY information explicitly present in the resume.
2. NEVER invent, guess, or assume information.
3. Do not add skills just because they are related to another skill.
4. Do not create experience that is not explicitly mentioned.
5. Do not create projects that are not explicitly mentioned.
6. If a field is not present, return an empty string or empty list.
7. Preserve the meaning of the original resume.
8. Skills should contain skills explicitly mentioned in the resume.
9. Education should contain the candidate's degrees, institutions, branches,
   years, CGPA/percentage, or other explicitly stated education details.
10. Experience should contain internships, jobs, or other professional experience.
11. Projects should contain explicitly mentioned academic, personal, or professional projects.
12. Certifications should contain explicitly mentioned certifications.
13. Return only data that can be supported by the resume text.

RESUME TEXT:
--------------------
{text}
--------------------
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ResumeData
            )
        )

        parsed_data = response.parsed

        if parsed_data is None:
            parsed_data = ResumeData.model_validate_json(response.text)

        return parsed_data.model_dump()

    except Exception as e:

        print("Gemini resume extraction failed:", e)

        # Return a safe empty structure instead of crashing the upload process
        return {
            "name": "",
            "email": "",
            "phone": "",
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": []
        }