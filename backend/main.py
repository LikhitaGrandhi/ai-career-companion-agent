from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import os
import shutil

from database.mongodb import test_connection, students_collection
from services.resume_parser import extract_text_from_pdf
from services.resume_extractor import extract_resume_data


app = FastAPI(
    title="AI Career Companion Agent",
    description="AI-powered internship matching and career assistance system",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MongoDB connection test
@app.on_event("startup")
def startup_event():
    test_connection()


# Home
@app.get("/")
def root():
    return {
        "message": "AI Career Companion Agent Backend is running!"
    }


# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Get all student profiles
@app.get("/students")
def get_students():

    students = list(students_collection.find())

    for student in students:
        student["_id"] = str(student["_id"])

    return students


# Upload, parse and SAVE resume
@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Check PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Create uploads folder
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Save PDF
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 1: Extract raw text
    extracted_text = extract_text_from_pdf(file_path)

    # Step 2: Extract structured resume data
    extracted_data = extract_resume_data(extracted_text)

    # Step 3: Save extracted data to MongoDB
    student_document = {
        "resume_filename": file.filename,
        "name": extracted_data.get("name"),
        "email": extracted_data.get("email"),
        "phone": extracted_data.get("phone"),
        "skills": extracted_data.get("skills", []),
        "education": extracted_data.get("education", []),
        "experience": extracted_data.get("experience", []),
        "projects": extracted_data.get("projects", []),
        "certifications": extracted_data.get("certifications", [])
    }

    result = students_collection.insert_one(student_document)

    return {
        "message": "Resume uploaded, parsed and saved successfully",
        "student_id": str(result.inserted_id),
        "filename": file.filename,
        "extracted_data": extracted_data
    }