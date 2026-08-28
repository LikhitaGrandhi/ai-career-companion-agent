from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI(
    title="AI Career Companion Agent",
    description="Backend for internship matching and interview preparation",
    version="1.0.0"
)


class StudentProfile(BaseModel):
    name: str
    email: str
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    skills: list[str] = []


@app.get("/")
def home():
    return {
        "message": "AI Career Companion Agent API is running"
    }


@app.post("/profile")
def create_profile(profile: StudentProfile):
    return {
        "message": "Student profile created successfully",
        "profile": profile
    }


@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "status": "ready for parsing"
    }


@app.get("/agents")
def get_agents():
    return {
        "agents": [
            "Resume Agent",
            "Job-Resume Matching Agent",
            "Skill Gap Agent",
            "Cover Letter Agent",
            "Interview Agent",
            "Career Assistant"
        ]
    }
