from pydantic import BaseModel
from typing import List, Optional


class StudentProfile(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    education: str
    college: str
    branch: str
    cgpa: Optional[float] = None
    skills: List[str] = []
    projects: List[str] = []
    experience: List[str] = []
    certifications: List[str] = []