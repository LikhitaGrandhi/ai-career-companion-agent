# ============================================================
# CAREER ASSISTANT AGENT
# ============================================================

def detect_intent(question):
    """
    Detect the user's career-related question intent.
    """

    question = question.lower().strip()

    # Skill gap questions
    skill_gap_keywords = [
    "skill gap",
    "skill gaps",
    "skill am i missing",
    "skills am i missing",
    "skill am i lacking",
    "skills am i lacking",
    "missing skill",
    "missing skills",
    "what skill",
    "what skills",
    "which skill",
    "which skills",
    "skills should i learn",
    "skill should i learn",
    "skills do i need",
    "skill do i need",
    "improve my skills",
    "improve my skill"
]

    if any(keyword in question for keyword in skill_gap_keywords):
        return "skill_gap"

    # Internship questions
    internship_keywords = [
        "internship",
        "internships",
        "job",
        "jobs",
        "role",
        "roles",
        "opportunities",
        "opportunity",
        "company",
        "companies"
    ]

    if any(keyword in question for keyword in internship_keywords):
        return "internship"

    # Resume questions
    resume_keywords = [
        "resume",
        "cv",
        "curriculum vitae",
        "resume score",
        "resume improve",
        "improve my resume"
    ]

    if any(keyword in question for keyword in resume_keywords):
        return "resume"

    # Interview questions
    interview_keywords = [
        "interview",
        "interview questions",
        "prepare for interview",
        "interview preparation",
        "technical questions",
        "hr questions",
        "behavioral questions"
    ]

    if any(keyword in question for keyword in interview_keywords):
        return "interview"

    # Cover letter
    cover_letter_keywords = [
        "cover letter",
        "application letter",
        "write a letter"
    ]

    if any(keyword in question for keyword in cover_letter_keywords):
        return "cover_letter"

    return "general"


# ============================================================
# GENERAL RESPONSE
# ============================================================

def generate_general_response(student):
    name = student.get("name", "there")

    return (
        f"Hi {name}! 👋 I am your AI Career Assistant. "
        "I can help you with internship matching, skill gaps, "
        "resume improvement, cover letters and interview preparation. "
        "Try asking something like: "
        "\"What skills am I missing?\", "
        "\"Which internships match my profile?\", or "
        "\"How should I prepare for an interview?\""
    )


# ============================================================
# INTERNSHIP RESPONSE
# ============================================================

def generate_internship_response(jobs):
    if not jobs:
        return (
            "I couldn't find internship matches for your profile "
            "right now. Try adding more relevant skills, projects "
            "or experience to your profile."
        )

    top_jobs = jobs[:5]

    response = "Here are some internship opportunities matching your profile:\n\n"

    for index, job in enumerate(top_jobs, start=1):
        title = job.get("job_title", "Internship")
        company = job.get("company", "Company")
        location = job.get("location", "Location")
        score = job.get("match_score")

        if score is not None:
            response += (
                f"{index}. {title} — {company} "
                f"({location}) — Match: {score}%\n"
            )
        else:
            response += (
                f"{index}. {title} — {company} "
                f"({location})\n"
            )

    return response


# ============================================================
# SKILL GAP RESPONSE
# ============================================================

def generate_skill_gap_response(skill_gap_results):
    if not skill_gap_results:
        return (
            "I couldn't calculate your current skill gaps. "
            "Please make sure your student profile contains "
            "your skills and that internship data is available."
        )

    missing_required = set()
    missing_preferred = set()

    for result in skill_gap_results:
        required_gaps = result.get(
            "critical_gaps",
            result.get("missing_required_skills", [])
        )

        preferred_gaps = result.get(
            "preferred_gaps",
            result.get("missing_preferred_skills", [])
        )

        if isinstance(required_gaps, list):
            missing_required.update(required_gaps)

        if isinstance(preferred_gaps, list):
            missing_preferred.update(preferred_gaps)

    response = "Based on your internship matches, here is your skill-gap summary:\n\n"

    if missing_required:
        response += "🔴 Important skills to improve:\n"

        for skill in sorted(missing_required):
            response += f"• {skill}\n"

        response += "\n"

    if missing_preferred:
        response += "🟡 Preferred skills you could strengthen:\n"

        for skill in sorted(missing_preferred):
            response += f"• {skill}\n"

        response += "\n"

    if not missing_required and not missing_preferred:
        response += (
            "🎉 No major skill gaps were identified "
            "for the analyzed internship roles.\n\n"
        )

    response += (
        "Recommended approach:\n"
        "• Learn one high-priority missing skill at a time.\n"
        "• Build a small project using the skill.\n"
        "• Add the project to your resume after completing it.\n"
        "• Practice interview questions related to the skill."
    )

    return response


# ============================================================
# RESUME RESPONSE
# ============================================================

def generate_resume_response(student):
    skills = student.get("skills", [])
    projects = student.get("projects", [])
    education = student.get("education", [])

    response = "Here is what I can see from your current profile:\n\n"

    if skills:
        response += "📌 Skills:\n"

        if isinstance(skills, list):
            for skill in skills:
                response += f"• {skill}\n"
        else:
            response += f"• {skills}\n"

        response += "\n"

    if projects:
        response += "📂 Projects:\n"

        if isinstance(projects, list):
            for project in projects:
                response += f"• {project}\n"
        else:
            response += f"• {projects}\n"

        response += "\n"

    if education:
        response += "🎓 Education:\n"

        if isinstance(education, list):
            for item in education:
                response += f"• {item}\n"
        else:
            response += f"• {education}\n"

        response += "\n"

    response += (
        "For internship applications, make sure your resume "
        "clearly highlights relevant skills, projects, education "
        "and measurable achievements."
    )

    return response


# ============================================================
# INTERVIEW RESPONSE
# ============================================================

def generate_interview_response():
    return (
        "For internship interviews, prepare in these areas:\n\n"
        "🎯 Technical\n"
        "• Programming fundamentals\n"
        "• Data structures and algorithms\n"
        "• Skills mentioned in the internship description\n\n"
        "📂 Projects\n"
        "• Problem your project solved\n"
        "• Technologies used\n"
        "• Your individual contribution\n"
        "• Challenges and solutions\n\n"
        "👤 HR / Behavioral\n"
        "• Tell me about yourself\n"
        "• Your strengths and weaknesses\n"
        "• Why this internship?\n"
        "• Career goals\n\n"
        "Practice explaining your projects clearly and concisely."
    )


# ============================================================
# COVER LETTER RESPONSE
# ============================================================

def generate_cover_letter_response():
    return (
        "Your cover letter should contain:\n\n"
        "1. A short introduction.\n"
        "2. The internship role you are applying for.\n"
        "3. Relevant technical skills.\n"
        "4. Relevant academic projects or experience.\n"
        "5. Why you are interested in the role.\n"
        "6. A short closing statement.\n\n"
        "Keep it concise and customize it for each internship."
    )


# ============================================================
# MAIN CAREER ASSISTANT FUNCTION
# ============================================================

def answer_career_question(
    question,
    student,
    jobs=None,
    skill_gap_results=None
):
    """
    Main Career Assistant function.

    Parameters:
        question: User's career question
        student: Student profile from MongoDB
        jobs: Internship matching results
        skill_gap_results: Skill gap analysis results

    Returns:
        Dictionary containing detected intent and response.
    """

    jobs = jobs or []
    skill_gap_results = skill_gap_results or []

    intent = detect_intent(question)

    if intent == "internship":
        response = generate_internship_response(jobs)

    elif intent == "skill_gap":
        response = generate_skill_gap_response(
            skill_gap_results
        )

    elif intent == "resume":
        response = generate_resume_response(student)

    elif intent == "interview":
        response = generate_interview_response()

    elif intent == "cover_letter":
        response = generate_cover_letter_response()

    else:
        response = generate_general_response(student)

    return {
        "intent": intent,
        "response": response
    }