def generate_technical_questions(student, job, count=5):
    """
    Generate technical questions based on the student's
    skills and the internship's required/preferred skills.
    """

    student_skills = student.get("skills", [])

    required_skills = job.get(
        "required_skills",
        ""
    )

    preferred_skills = job.get(
        "preferred_skills",
        ""
    )

    questions = []

    # Questions based on student's actual skills
    for skill in student_skills:
        questions.append(
            f"Explain your understanding of {skill} "
            f"and how you have used it."
        )

    # Questions based on job requirements
    if required_skills:
        questions.append(
            f"What is your approach to working with "
            f"the required skills mentioned for this role: "
            f"{required_skills}?"
        )

    if preferred_skills:
        questions.append(
            f"Which of these preferred skills would you "
            f"like to strengthen: {preferred_skills}?"
        )

    return questions[:count]


def generate_project_questions(student, count=5):
    """
    Generate questions based only on projects
    provided by the student.
    """

    projects = student.get(
        "projects",
        []
    )

    questions = []

    for project in projects:
        questions.append(
            f"Explain the {project} project. "
            f"What problem did it solve?"
        )

        questions.append(
            f"What technologies did you use in "
            f"{project}, and why?"
        )

        questions.append(
            f"What challenges did you face while "
            f"developing {project}?"
        )

    return questions[:count]


def generate_role_questions(job, count=5):
    """
    Generate questions specific to the selected role.
    """

    job_title = job.get(
        "job_title",
        "this internship"
    )

    company = job.get(
        "company",
        "the organization"
    )

    questions = [
        f"Why are you interested in the {job_title} role?",

        f"What do you understand about the responsibilities "
        f"of a {job_title}?",

        f"How would you contribute to {company} "
        f"as an intern?",

        f"How would you approach a technical problem "
        f"related to the {job_title} role?",

        f"What would you like to learn during this internship?"
    ]

    return questions[:count]


def generate_hr_questions(student, job, count=5):
    """
    Generate general HR and behavioral questions.
    """

    questions = [
        "Tell me about yourself.",

        "What are your strengths?",

        "Describe a technical challenge you faced "
        "and how you handled it.",

        "How do you manage your time when working "
        "on multiple tasks?",

        "Where do you see yourself developing "
        "professionally through this internship?"
    ]

    return questions[:count]


def generate_interview_plan(student, job):
    """
    Create a complete interview preparation plan.
    """

    technical_questions = generate_technical_questions(
        student,
        job
    )

    project_questions = generate_project_questions(
        student
    )

    role_questions = generate_role_questions(
        job
    )

    hr_questions = generate_hr_questions(
        student,
        job
    )

    return {
        "job_title": job.get(
            "job_title",
            "Internship"
        ),

        "company": job.get(
            "company",
            ""
        ),

        "technical_questions": technical_questions,

        "project_questions": project_questions,

        "role_questions": role_questions,

        "hr_questions": hr_questions,

        "preparation_tips": [
            "Review the required skills listed for the role.",
            "Be prepared to explain every project on your resume.",
            "Revise fundamental concepts related to the internship.",
            "Prepare examples of technical problems you solved.",
            "Practice explaining your answers clearly and concisely."
        ]
    }


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

        "projects": [
            "AI Resume Analyzer",
            "Railway Reservation System"
        ]
    }

    job = {
        "job_id": "JOB-001",

        "job_title": "Machine Learning Intern",

        "company": "ApexGrid",

        "required_skills": (
            "Python, NumPy, Pandas, "
            "Scikit-learn, Machine Learning"
        ),

        "preferred_skills": (
            "Deep Learning, TensorFlow"
        )
    }

    interview_plan = generate_interview_plan(
        student,
        job
    )

    print("\n========== INTERVIEW PREPARATION ==========\n")

    print(
        "Role:",
        interview_plan["job_title"]
    )

    print(
        "Company:",
        interview_plan["company"]
    )

    print("\n--- Technical Questions ---")

    for i, question in enumerate(
        interview_plan["technical_questions"],
        1
    ):
        print(f"{i}. {question}")

    print("\n--- Project Questions ---")

    for i, question in enumerate(
        interview_plan["project_questions"],
        1
    ):
        print(f"{i}. {question}")

    print("\n--- Role Questions ---")

    for i, question in enumerate(
        interview_plan["role_questions"],
        1
    ):
        print(f"{i}. {question}")

    print("\n--- HR Questions ---")

    for i, question in enumerate(
        interview_plan["hr_questions"],
        1
    ):
        print(f"{i}. {question}")

    print("\n--- Preparation Tips ---")

    for tip in interview_plan["preparation_tips"]:
        print("-", tip)