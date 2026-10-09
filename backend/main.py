from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from fastapi.middleware.cors import CORSMiddleware

import os

import shutil

from backend.models.auth import (

    SignupRequest,

    SignupResponse,

    LoginRequest,

    LoginResponse

)

from bson import ObjectId

from backend.services.auth_service import (

    create_user,

    login_user

)

from backend.agents.job_resume_matcher import match_student_to_jobs

from backend.agents.skill_gap_agent import analyze_skill_gap

from backend.models.conversation import ConversationMessage

from backend.agents.resume_customization_agent import (

    customize_resume,

    generate_cover_letter

)

from backend.services.document_storage import save_document

from backend.services.conversation_service import (

    get_conversation,

    add_message,

    clear_conversation

)

from backend.agents.interview_agent import generate_interview_plan

from backend.agents.career_assistant import answer_career_question

from backend.database.mongodb import (

    test_connection,

    students_collection,

    db

)

users_collection = db["users"]

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

@app.post("/auth/login", response_model=LoginResponse)

def login(user: LoginRequest):

    logged_in_user = login_user(

        user.email,

        user.password

    )

    if logged_in_user is None:

        raise HTTPException(

            status_code=401,

            detail="Invalid email or password"

        )

    return {

        "message": "Login successful",

        "user_id": logged_in_user["user_id"],

        "name": logged_in_user["name"],

        "student_id": logged_in_user.get("student_id")

    }

@app.post("/auth/signup", response_model=SignupResponse)

def signup(user: SignupRequest):

    user_id = create_user(

        user.name,

        user.email,

        user.password

    )

    if user_id is None:

        raise HTTPException(

            status_code=400,

            detail="Email already registered"

        )

    return {

        "message": "Account created successfully",

        "user_id": user_id

    }

from backend.models.conversation import ConversationMessage

# =========================================================

# CAREER ASSISTANT CONVERSATION MEMORY

# =========================================================

conversation_history = {}

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

    students = list(students_collection.find())

    for student in students:

        student["_id"] = str(student["_id"])

    return students

# =========================================================

# GET ONE STUDENT PROFILE BY ID

# =========================================================

@app.get("/students/{student_id}")

def get_student_by_id(student_id: str):

    try:

        student = students_collection.find_one(

            {"_id": ObjectId(student_id)}

        )

        if student is None:

            raise HTTPException(

                status_code=404,

                detail="Student profile not found"

            )

        student["_id"] = str(student["_id"])

        return student

    except HTTPException:

        raise

    except Exception:

        raise HTTPException(

            status_code=400,

            detail="Invalid student ID"

        )

# =========================================================

# UPLOAD, PARSE AND SAVE RESUME

# =========================================================

@app.post("/resume/upload")

async def upload_resume(

    user_id: str = Form(...),

    file: UploadFile = File(...)

):

    # Check PDF

    if not file.filename or not file.filename.lower().endswith(".pdf"):

        raise HTTPException(

            status_code=400,

            detail="Only PDF files are allowed"

        )

    # Validate user ID

    try:

        user_object_id = ObjectId(user_id)

    except Exception:

        raise HTTPException(

            status_code=400,

            detail="Invalid user ID"

        )

    user = users_collection.find_one({"_id": user_object_id})

    if user is None:

        raise HTTPException(

            status_code=404,

            detail="User account not found"

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

    # Step 3: Build student profile

    student_document = {

        "user_id": user_id,

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

    # Save student profile

    result = students_collection.insert_one(student_document)

    student_id = str(result.inserted_id)

    # Link profile to user account

    users_collection.update_one(

        {"_id": user_object_id},

        {"$set": {"student_id": student_id}}

    )

    return {

        "message": "Resume uploaded, parsed and saved successfully",

        "student_id": student_id,

        "filename": file.filename,

        "extracted_data": extracted_data

    }

# =========================================================

# UPLOAD, PARSE AND SAVE RESUME

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

        # Save generated resume

        resume_id = save_document(

            student_id=student_id,

            document_type="resume",

            job_id=job_id,

            content=customized_resume

        )

        return {

            "student_id": student_id,

            "job_id": job_id,

            "resume_id": resume_id,

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

        # Save generated cover letter

        cover_letter_id = save_document(

            student_id=student_id,

            document_type="cover_letter",

            job_id=job_id,

            content=cover_letter

        )

        return {

            "student_id": student_id,

            "job_id": job_id,

            "cover_letter_id": cover_letter_id,

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

        # Get previous conversation history

        # -------------------------------------------------

        history = get_conversation(student_id)

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

        # Save current user message

        # -------------------------------------------------

        add_message(

            student_id=student_id,

            role="user",

            message=question

        )

        # -------------------------------------------------

        # Ask Career Assistant

        # -------------------------------------------------

        result = answer_career_question(

            question=question,

            student=student,

            jobs=internship_matches,

            skill_gap_results=skill_gap_results,

            conversation_history=history

        )

        # -------------------------------------------------

        # Save assistant response

        # -------------------------------------------------

        add_message(

            student_id=student_id,

            role="assistant",

            message=result["response"]

        )

        # -------------------------------------------------

        # Get updated conversation

        # -------------------------------------------------

        updated_history = get_conversation(

            student_id

        )

        # -------------------------------------------------

        # Return response

        # -------------------------------------------------

        return {

            "student_id": student_id,

            "question": question,

            "intent": result["intent"],

            "response": result["response"],

            "conversation_history": [

                {

                    "role": message.role,

                    "message": message.message,

                    "timestamp": message.timestamp

                }

                for message in updated_history

            ]

        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )

# =========================================================

# M4 — APPLICATION TRACKING

# =========================================================

from backend.models.application import ApplicationCreate, ApplicationUpdate

from backend.services.application_tracker import (

    create_application,

    get_application,

    get_student_applications,

    update_application,

    delete_application,

    get_application_dashboard,

    APPLICATION_STATUSES,

)

@app.post("/applications/{student_id}")

def add_application(

    student_id: str,

    application: ApplicationCreate

):

    try:

        application_data = application.model_dump()

        if application_data.get("status") not in APPLICATION_STATUSES:

            raise HTTPException(

                status_code=400,

                detail=f"Invalid status. Allowed statuses: {APPLICATION_STATUSES}"

            )

        application_id = create_application(

            student_id,

            application_data

        )

        return {

            "message": "Application added successfully",

            "application_id": application_id

        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )

@app.get("/applications/{student_id}")

def list_applications(

    student_id: str,

    status: str = None,

    company: str = None,

    search: str = None

):

    try:

        applications = get_student_applications(

            student_id=student_id,

            status=status,

            company=company,

            search=search

        )

        return {

            "student_id": student_id,

            "count": len(applications),

            "applications": applications

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )

@app.get("/applications/{student_id}/dashboard")

def application_dashboard(student_id: str):

    try:

        dashboard = get_application_dashboard(student_id)

        return {

            "student_id": student_id,

            **dashboard

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )

@app.get("/application/{student_id}/{application_id}")

def get_single_application(

    student_id: str,

    application_id: str

):

    try:

        application = get_application(

            application_id,

            student_id

        )

        if not application:

            raise HTTPException(

                status_code=404,

                detail="Application not found"

            )

        return application

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )

@app.put("/application/{student_id}/{application_id}")

def edit_application(

    student_id: str,

    application_id: str,

    application: ApplicationUpdate

):

    try:

        update_data = {

            key: value

            for key, value in application.model_dump().items()

            if value is not None

        }

        if "status" in update_data:

            if update_data["status"] not in APPLICATION_STATUSES:

                raise HTTPException(

                    status_code=400,

                    detail=f"Invalid status. Allowed statuses: {APPLICATION_STATUSES}"

                )

        updated_application = update_application(

            application_id,

            student_id,

            update_data

        )

        if not updated_application:

            raise HTTPException(

                status_code=404,

                detail="Application not found"

            )

        return {

            "message": "Application updated successfully",

            "application": updated_application

        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )

@app.delete("/application/{student_id}/{application_id}")

def remove_application(

    student_id: str,

    application_id: str

):

    try:

        deleted = delete_application(

            application_id,

            student_id

        )

        if not deleted:

            raise HTTPException(

                status_code=404,

                detail="Application not found"

            )

        return {

            "message": "Application deleted successfully"

        }

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
