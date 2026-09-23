from backend.agents.skill_gap_agent import analyze_skill_gap

from backend.agents.resume_customization_agent import (
    customize_resume,
    generate_cover_letter
)

from backend.agents.interview_agent import (
    generate_interview_plan
)


def career_assistant(student, job, user_query):
    """
    Conversational Career Assistant.

    Routes the user's question to the appropriate
    career-support functionality:

    1. Skill Gap Analysis
    2. Resume Customization
    3. Cover Letter Generation
    4. Interview Preparation
    5. Job/Internship Information
    6. General Career Assistance
    """

    query = user_query.lower().strip()

    # ==================================================
    # 1. SKILL GAP ANALYSIS
    # ==================================================

    if (
        "skill gap" in query
        or "missing skill" in query
        or "missing skills" in query
        or "skills am i missing" in query
        or "skills are missing" in query
        or "what skills am i missing" in query
        or "skills do i need" in query
        or "skills should i learn" in query
        or "what should i learn" in query
    ):

        analysis = analyze_skill_gap(
            student,
            job
        )

        return {
            "intent": "skill_gap",

            "response": (
                f"For the "
                f"{job.get('job_title', 'selected role')} "
                f"position, your required-skill match is "
                f"{analysis['required_skill_match_percentage']}%."
            ),

            "data": analysis
        }

    # ==================================================
    # 2. RESUME CUSTOMIZATION
    # ==================================================

    if (
        "resume" in query
        or "cv" in query
        or "customize my resume" in query
        or "tailor my resume" in query
        or "improve my resume" in query
    ):

        resume = customize_resume(
            student,
            job
        )

        return {
            "intent": "resume",

            "response": (
                f"Here is a customized resume draft "
                f"for the "
                f"{job.get('job_title', 'selected role')} role."
            ),

            "data": resume
        }

    # ==================================================
    # 3. COVER LETTER
    # ==================================================

    if (
        "cover letter" in query
        or "application letter" in query
        or "write a cover letter" in query
        or "generate a cover letter" in query
    ):

        cover_letter = generate_cover_letter(
            student,
            job
        )

        return {
            "intent": "cover_letter",

            "response": (
                f"Here is a cover letter draft for "
                f"{job.get('company', 'the selected company')}."
            ),

            "data": {
                "cover_letter": cover_letter
            }
        }

    # ==================================================
    # 4. INTERVIEW PREPARATION
    # ==================================================

    if (
        "interview" in query
        or "interview questions" in query
        or "prepare for interview" in query
        or "prepare me" in query
        or "interview preparation" in query
        or "how should i prepare" in query
    ):

        interview_plan = generate_interview_plan(
            student,
            job
        )

        return {
            "intent": "interview",

            "response": (
                f"Here is your interview preparation "
                f"plan for the "
                f"{job.get('job_title', 'selected role')} role."
            ),

            "data": interview_plan
        }

    # ==================================================
    # 5. JOB / INTERNSHIP INFORMATION
    # ==================================================

    if (
        "job" in query
        or "role" in query
        or "internship" in query
        or "responsibilities" in query
        or "requirements" in query
        or "job requirements" in query
        or "tell me about this internship" in query
    ):

        return {
            "intent": "job_information",

            "response": (
                f"You are currently exploring the "
                f"{job.get('job_title', 'selected role')} "
                f"position at "
                f"{job.get('company', 'the selected company')}."
            ),

            "data": {
                "job_title": job.get("job_title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "description": job.get("description"),
                "responsibilities": job.get("responsibilities"),
                "required_skills": job.get("required_skills"),
                "preferred_skills": job.get("preferred_skills"),
                "qualifications": job.get("qualifications"),
                "experience": job.get("experience"),
                "education": job.get("education")
            }
        }

    # ==================================================
    # 6. GENERAL CAREER ASSISTANCE
    # ==================================================

    return {
        "intent": "general",

        "response": (
            "I can help you with internship matching, "
            "skill-gap analysis, resume customization, "
            "cover letters, interview preparation, "
            "and internship requirements."
        ),

        "data": {}
    }


# ======================================================
# TESTING
# ======================================================

if __name__ == "__main__":

    student = {
        "name": "Likhita",

        "skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "SQL",
            "Java"
        ],

        "education": (
            "B.Tech in Artificial Intelligence "
            "and Data Science"
        ),

        "experience": [],

        "projects": [
            "AI Resume Analyzer",
            "Railway Reservation System"
        ]
    }


    job = {
        "job_id": "JOB-001",

        "job_title": "Machine Learning Intern",

        "company": "ApexGrid",

        "location": "Bengaluru",

        "description": (
            "Machine learning internship involving "
            "data analysis and model development."
        ),

        "responsibilities": (
            "Build machine learning models, "
            "analyze datasets and evaluate models."
        ),

        "required_skills": (
            "Python, NumPy, Pandas, "
            "Scikit-learn, Machine Learning"
        ),

        "preferred_skills": (
            "Deep Learning, TensorFlow"
        ),

        "qualifications": (
            "Strong programming and analytical skills"
        ),

        "experience": "0-1 years",

        "education": (
            "Bachelor's degree in Computer Science, "
            "AI, Data Science or related field"
        )
    }


    print("\n========== CAREER ASSISTANT ==========\n")


    queries = [

        "What skills am I missing?",

        "Help me customize my resume",

        "Write a cover letter",

        "Prepare me for the interview",

        "Tell me about this internship",

        "What are the requirements for this job?",

        "What can you help me with?"
    ]


    for query in queries:

        result = career_assistant(
            student,
            job,
            query
        )

        print(f"\nUser: {query}")

        print(
            f"Intent: {result['intent']}"
        )

        print(
            f"Assistant: {result['response']}"
        )