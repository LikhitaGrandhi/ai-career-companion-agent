from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    company_name: str
    job_title: str
    job_description: Optional[str] = ""
    
    application_date: Optional[str] = None
    deadline: Optional[str] = None

    status: str = "Saved"

    interview_date: Optional[str] = None
    interview_status: Optional[str] = ""

    notes: Optional[str] = ""

    resume_id: Optional[str] = None
    cover_letter_id: Optional[str] = None


class ApplicationUpdate(BaseModel):
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    job_description: Optional[str] = None

    application_date: Optional[str] = None
    deadline: Optional[str] = None

    status: Optional[str] = None

    interview_date: Optional[str] = None
    interview_status: Optional[str] = None

    notes: Optional[str] = None

    resume_id: Optional[str] = None
    cover_letter_id: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: str
    student_id: str

    company_name: str
    job_title: str
    job_description: str

    application_date: Optional[str]
    deadline: Optional[str]

    status: str

    interview_date: Optional[str]
    interview_status: Optional[str]

    notes: str

    resume_id: Optional[str]
    cover_letter_id: Optional[str]

    created_at: datetime
    updated_at: datetime