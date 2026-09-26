from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import os
import shutil
from backend.agents.job_resume_matcher import match_student_to_jobs
from backend.agents.skill_gap_agent import analyze_skill_gap
from backend.agents.resume_customization_agent import (
    customize_resume,
    generate_cover_letter
)
from backend.agents.interview_agent import generate_interview_plan
from backend.agents.career_assistant import answer_career_question

from backend.database.mongodb import (
    test_connection,
    students_collection
)

from backend.services.resume_parser import (
    extract_text_from_pdf
)

from backend.services.resume_extractor import (
    extract_resume_data
)

from backend.rag.search_jobs import search_jobs


app = FastAPI(
    title="AI Career Companion Agent",
    description="AI-powered internship matching and career assistance system",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# MONGODB CONNECTION TEST
# =========================================================

@app.on_event("startup")
def startup_event():
    test_connection()


# =========================================================
# HOME
# =========================================================

@app.get("/")
def root():
    return {
        "message": "AI Career Companion Agent Backend is running!"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# GET ALL STUDENT PROFILES
# =========================================================

@app.get("/students")
def get_students():

    students = list(
        students_collection.find()
    )

    for student in students:
        student["_id"] = str(
            student["_id"]
        )

    return students


# =========================================================
# UPLOAD, PARSE AND SAVE RESUME
# =========================================================

@app.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...)
):

    # Check PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Create uploads folder
    upload_dir = "uploads"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    # Save PDF
    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # -----------------------------------------------------
    # Step 1: Extract raw text
    # -----------------------------------------------------

    extracted_text = extract_text_from_pdf(
        file_path
    )

    # -----------------------------------------------------
    # Step 2: Extract structured resume data
    # -----------------------------------------------------

    extracted_data = extract_resume_data(
        extracted_text
    )

    # -----------------------------------------------------
    # Step 3: Save extracted data to MongoDB
    # -----------------------------------------------------

    student_document = {
        "resume_filename": file.filename,

        "name": extracted_data.get(
            "name"
        ),

        "email": extracted_data.get(
            "email"
        ),

        "phone": extracted_data.get(
            "phone"
        ),

        "skills": extracted_data.get(
            "skills",
            []
        ),

        "education": extracted_data.get(
            "education",
            []
        ),

        "experience": extracted_data.get(
            "experience",
            []
        ),

        "projects": extracted_data.get(
            "projects",
            []
        ),

        "certifications": extracted_data.get(
            "certifications",
            []
        )
    }

    result = students_collection.insert_one(
        student_document
    )

    return {
        "message": "Resume uploaded, parsed and saved successfully",

        "student_id": str(
            result.inserted_id
        ),

        "filename": file.filename,

        "extracted_data": extracted_data
    }


# =========================================================
# INTERNSHIP MATCHING
# =========================================================

@app.get("/internships/{student_id}")
def get_internship_matches(
    student_id: str
):

    from bson import ObjectId

    try:

        # -------------------------------------------------
        # Find student
        # -------------------------------------------------

        student = students_collection.find_one(
            {
                "_id": ObjectId(
                    student_id
                )
            }
        )

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        # -------------------------------------------------
        # Create student text
        # -------------------------------------------------

        student_text = " ".join([
            str(
                student.get(
                    "name",
                    ""
                )
            ),

            str(
                student.get(
                    "skills",
                    ""
                )
            ),

            str(
                student.get(
                    "education",
                    ""
                )
            ),

            str(
                student.get(
                    "experience",
                    ""
                )
            ),

            str(
                student.get(
                    "projects",
                    ""
                )
            )
        ])

        # -------------------------------------------------
        # Retrieve relevant jobs from FAISS
        # -------------------------------------------------

        retrieved_jobs = search_jobs(
            student_text,
            top_k=10
        )

        # -------------------------------------------------
        # Match jobs with student
        # -------------------------------------------------

        matches = match_student_to_jobs(
            student,
            retrieved_jobs
        )

        return {
            "student_id": student_id,

            "total_matches": len(
                matches
            ),

            "matches": matches
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# SKILL GAP ANALYSIS
# =========================================================

@app.get("/skill-gap/{student_id}")
def get_skill_gap(
    student_id: str
):

    from bson import ObjectId

    try:

        # -------------------------------------------------
        # Find student
        # -------------------------------------------------

        student = students_collection.find_one(
            {
                "_id": ObjectId(
                    student_id
                )
            }
        )

        if not student:

            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        # -------------------------------------------------
        # Create student text for semantic search
        # -------------------------------------------------

        student_text = " ".join([
            str(
                student.get(
                    "name",
                    ""
                )
            ),

            str(
                student.get(
                    "skills",
                    ""
                )
            ),

            str(
                student.get(
                    "education",
                    ""
                )
            ),

            str(
                student.get(
                    "experience",
                    ""
                )
            ),

            str(
                student.get(
                    "projects",
                    ""
                )
            )
        ])

        # -------------------------------------------------
        # Retrieve relevant internships
        # -------------------------------------------------

        retrieved_jobs = search_jobs(
            student_text,
            top_k=10
        )

        # -------------------------------------------------
        # Analyze skill gaps
        # -------------------------------------------------

        skill_gap_results = []

        for job in retrieved_jobs:

            analysis = analyze_skill_gap(
                student,
                job
            )

            # Add semantic similarity
            analysis["similarity_score"] = round(
                float(
                    job.get(
                        "similarity_score",
                        0
                    )
                ),
                4
            )

            skill_gap_results.append(
                analysis
            )

        # -------------------------------------------------
        # Return results
        # -------------------------------------------------

        return {
            "student_id": student_id,

            "total_jobs_analyzed": len(
                skill_gap_results
            ),

            "results": skill_gap_results
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# RESUME CUSTOMIZATION
# =========================================================

@app.post("/resume/customize")
def customize_student_resume(
    student_id: str,
    job_id: str
):
    from bson import ObjectId

    try:

        # Find student
        student = students_collection.find_one(
            {
                "_id": ObjectId(student_id)
            }
        )

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        # Search internship jobs
        student_text = " ".join([
            str(student.get("name", "")),
            str(student.get("skills", "")),
            str(student.get("education", "")),
            str(student.get("experience", "")),
            str(student.get("projects", ""))
        ])

        jobs = search_jobs(
            student_text,
            top_k=60
        )

        # Find requested job
        selected_job = None

        for job in jobs:
            if job.get("job_id") == job_id:
                selected_job = job
                break

        if not selected_job:
            raise HTTPException(
                status_code=404,
                detail="Internship job not found"
            )

        # Generate customized resume
        customized_resume = customize_resume(
            student,
            selected_job
        )

        return {
            "student_id": student_id,
            "job_id": job_id,
            "customized_resume": customized_resume
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# COVER LETTER GENERATION
# =========================================================

@app.post("/cover-letter/generate")
def generate_cover_letter_endpoint(
    student_id: str,
    job_id: str
):
    from bson import ObjectId

    try:

        # Find student
        student = students_collection.find_one(
            {
                "_id": ObjectId(student_id)
            }
        )

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        # Create student text
        student_text = " ".join([
            str(student.get("name", "")),
            str(student.get("skills", "")),
            str(student.get("education", "")),
            str(student.get("experience", "")),
            str(student.get("projects", ""))
        ])

        # Retrieve jobs
        jobs = search_jobs(
            student_text,
            top_k=60
        )

        # Find selected job
        selected_job = None

        for job in jobs:
            if job.get("job_id") == job_id:
                selected_job = job
                break

        if not selected_job:
            raise HTTPException(
                status_code=404,
                detail="Internship job not found"
            )

        # Generate cover letter
        cover_letter = generate_cover_letter(
            student,
            selected_job
        )

        return {
            "student_id": student_id,
            "job_id": job_id,
            "cover_letter": cover_letter
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.get("/interview-prep/{student_id}/{job_id}")
def get_interview_prep(student_id: str, job_id: str):
    from bson import ObjectId

    try:
        # Get student
        student = students_collection.find_one(
            {"_id": ObjectId(student_id)}
        )

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        # Build student text for job retrieval
        student_text = " ".join([
            str(student.get("name", "")),
            str(student.get("skills", "")),
            str(student.get("education", "")),
            str(student.get("experience", "")),
            str(student.get("projects", ""))
        ])

        # Retrieve available jobs
        jobs = search_jobs(
            student_text,
            top_k=60
        )

        # Find selected job
        selected_job = None

        for job in jobs:
            if job.get("job_id") == job_id:
                selected_job = job
                break

        if not selected_job:
            raise HTTPException(
                status_code=404,
                detail="Internship job not found"
            )

        # Generate interview preparation plan
        interview_plan = generate_interview_plan(
            student,
            selected_job
        )

        return {
            "student_id": student_id,
            "job_id": job_id,
            "interview_plan": interview_plan
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# AI CAREER ASSISTANT
# =========================================================

@app.post("/career-assistant/{student_id}")
def career_assistant(
    student_id: str,
    question: str
):
    from bson import ObjectId

    try:

        # -------------------------------------------------
        # Find student
        # -------------------------------------------------

        student = students_collection.find_one(
            {
                "_id": ObjectId(student_id)
            }
        )

        if not student:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        # -------------------------------------------------
        # Create student text
        # -------------------------------------------------

        student_text = " ".join([
            str(student.get("name", "")),
            str(student.get("skills", "")),
            str(student.get("education", "")),
            str(student.get("experience", "")),
            str(student.get("projects", ""))
        ])

        # -------------------------------------------------
        # Retrieve internship matches
        # -------------------------------------------------

        retrieved_jobs = search_jobs(
            student_text,
            top_k=10
        )

        # -------------------------------------------------
        # Generate internship match results
        # -------------------------------------------------

        internship_matches = match_student_to_jobs(
            student,
            retrieved_jobs
        )

        # -------------------------------------------------
        # Generate skill-gap results
        # -------------------------------------------------

        skill_gap_results = []

        for job in retrieved_jobs:

            analysis = analyze_skill_gap(
                student,
                job
            )

            skill_gap_results.append(
                analysis
            )

        # -------------------------------------------------
        # Ask Career Assistant
        # -------------------------------------------------

        result = answer_career_question(
            question=question,
            student=student,
            jobs=internship_matches,
            skill_gap_results=skill_gap_results
        )

        # -------------------------------------------------
        # Return response
        # -------------------------------------------------

        return {
            "student_id": student_id,
            "question": question,
            "intent": result["intent"],
            "response": result["response"]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )