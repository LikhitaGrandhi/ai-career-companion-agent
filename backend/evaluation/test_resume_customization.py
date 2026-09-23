from backend.agents.resume_customization_agent import (
    customize_resume,
    generate_cover_letter
)


def evaluate_resume_customization(student, job):

    resume = customize_resume(student, job)
    cover_letter = generate_cover_letter(student, job)

    # Check that required sections exist
    required_sections = [
        "candidate_name",
        "target_role",
        "company",
        "professional_summary",
        "relevant_skills",
        "education",
        "experience",
        "projects"
    ]

    sections_present = all(
        section in resume
        for section in required_sections
    )

    # Check that only student skills are used
    student_skills = {
        skill.lower()
        for skill in student.get("skills", [])
    }

    resume_skills = {
        skill.lower()
        for skill in resume.get("relevant_skills", [])
    }

    no_invented_skills = resume_skills.issubset(
        student_skills
    )

    # Check cover letter
    cover_letter_generated = (
        len(cover_letter.strip()) > 0
        and student.get("name", "Candidate") in cover_letter
        and job.get("company", "") in cover_letter
    )

    return {
        "sections_present": sections_present,
        "no_invented_skills": no_invented_skills,
        "cover_letter_generated": cover_letter_generated,
        "overall_pass": (
            sections_present
            and no_invented_skills
            and cover_letter_generated
        )
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

        "required_skills": (
            "Python, NumPy, Pandas, "
            "Scikit-learn, Machine Learning"
        ),

        "preferred_skills": (
            "Deep Learning, TensorFlow"
        )
    }

    result = evaluate_resume_customization(
        student,
        job
    )

    print(
        "Resume sections present:",
        result["sections_present"]
    )

    print(
        "No invented skills:",
        result["no_invented_skills"]
    )

    print(
        "Cover letter generated:",
        result["cover_letter_generated"]
    )

    print(
        "\nOverall M3.2 Result:",
        "PASS" if result["overall_pass"] else "FAIL"
    )