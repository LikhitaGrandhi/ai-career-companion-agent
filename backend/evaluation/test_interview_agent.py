from backend.agents.interview_agent import generate_interview_plan


def evaluate_interview_agent(student, job):

    plan = generate_interview_plan(
        student,
        job
    )

    # Check all required sections
    required_sections = [
        "job_title",
        "company",
        "technical_questions",
        "project_questions",
        "role_questions",
        "hr_questions",
        "preparation_tips"
    ]

    sections_present = all(
        section in plan
        for section in required_sections
    )

    # Check that questions were generated
    technical_generated = (
        len(plan["technical_questions"]) > 0
    )

    project_generated = (
        len(plan["project_questions"]) > 0
    )

    role_generated = (
        len(plan["role_questions"]) > 0
    )

    hr_generated = (
        len(plan["hr_questions"]) > 0
    )

    tips_generated = (
        len(plan["preparation_tips"]) > 0
    )

    # Check that student's actual skills
    # appear in technical preparation
    technical_text = " ".join(
        plan["technical_questions"]
    ).lower()

    skill_reference_found = any(
        skill.lower() in technical_text
        for skill in student.get("skills", [])
    )

    # Check that student's projects
    # appear in project questions
    project_text = " ".join(
        plan["project_questions"]
    ).lower()

    project_reference_found = any(
        project.lower() in project_text
        for project in student.get("projects", [])
    )

    overall_pass = all([
        sections_present,
        technical_generated,
        project_generated,
        role_generated,
        hr_generated,
        tips_generated,
        skill_reference_found,
        project_reference_found
    ])

    return {
        "sections_present": sections_present,
        "technical_questions_generated": technical_generated,
        "project_questions_generated": project_generated,
        "role_questions_generated": role_generated,
        "hr_questions_generated": hr_generated,
        "preparation_tips_generated": tips_generated,
        "student_skills_referenced": skill_reference_found,
        "student_projects_referenced": project_reference_found,
        "overall_pass": overall_pass
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

    result = evaluate_interview_agent(
        student,
        job
    )



    print(
        "Sections present:",
        result["sections_present"]
    )

    print(
        "Technical questions generated:",
        result["technical_questions_generated"]
    )

    print(
        "Project questions generated:",
        result["project_questions_generated"]
    )

    print(
        "Role questions generated:",
        result["role_questions_generated"]
    )

    print(
        "HR questions generated:",
        result["hr_questions_generated"]
    )

    print(
        "Preparation tips generated:",
        result["preparation_tips_generated"]
    )

    print(
        "Student skills referenced:",
        result["student_skills_referenced"]
    )

    print(
        "Student projects referenced:",
        result["student_projects_referenced"]
    )

    print(
        "\nOverall M3.3 Result:",
        "PASS" if result["overall_pass"] else "FAIL"
    )