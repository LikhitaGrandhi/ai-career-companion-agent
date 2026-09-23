import re


def normalize_skill(skill):
    skill = skill.lower().strip()

    aliases = {
        "ml": "machine learning",
        "ai/ml": "machine learning",
        "sklearn": "scikit-learn",
        "scikit learn": "scikit-learn",
        "js": "javascript",
        "node": "node.js",
        "nodejs": "node.js",
        "reactjs": "react",
        "postgres": "postgresql",
    }

    return aliases.get(skill, skill)


def extract_skills(text):
    """
    Extract skills from comma/semicolon/pipe separated text.
    """
    if not text:
        return set()

    items = re.split(r"[,|;]", str(text))

    return {
        normalize_skill(item)
        for item in items
        if item.strip()
    }


def get_student_skills(student):
    """
    Get normalized skills from student profile.
    """
    skills = student.get("skills", [])

    if isinstance(skills, list):
        return {
            normalize_skill(skill)
            for skill in skills
            if skill
        }

    return extract_skills(skills)


def get_job_skills(job):
    """
    Extract required and preferred skills from job.
    """
    required_skills = extract_skills(
        job.get("required_skills", "")
    )

    preferred_skills = extract_skills(
        job.get("preferred_skills", "")
    )

    return required_skills, preferred_skills


def find_relevant_skills(student, job):
    """
    Find skills from the student's profile that are
    relevant to the selected internship.
    """

    student_skills = get_student_skills(student)

    required_skills, preferred_skills = get_job_skills(job)

    relevant_skills = (
        student_skills
        & (required_skills | preferred_skills)
    )

    return sorted(relevant_skills)


def customize_resume(student, job):
    """
    Generate a structured customized resume draft
    using only information available in the student profile.
    """

    relevant_skills = find_relevant_skills(student, job)

    student_name = student.get("name", "Candidate")

    education = student.get(
        "education",
        "Education details not provided"
    )

    experience = student.get(
        "experience",
        []
    )

    projects = student.get(
        "projects",
        []
    )

    resume = {
        "candidate_name": student_name,

        "target_role": job.get(
            "job_title",
            "Internship"
        ),

        "company": job.get(
            "company",
            ""
        ),

        "professional_summary": (
            f"{student_name} is a candidate interested in the "
            f"{job.get('job_title', 'internship')} role at "
            f"{job.get('company', 'the organization')}. "
            f"The candidate has relevant skills in "
            f"{', '.join(relevant_skills) if relevant_skills else 'the listed technical areas'}."
        ),

        "relevant_skills": relevant_skills,

        "education": education,

        "experience": experience,

        "projects": projects
    }

    return resume


def generate_cover_letter(student, job):
    """
    Generate a personalized cover letter draft
    without inventing candidate information.
    """

    student_name = student.get(
        "name",
        "Candidate"
    )

    job_title = job.get(
        "job_title",
        "Internship"
    )

    company = job.get(
        "company",
        "your organization"
    )

    relevant_skills = find_relevant_skills(
        student,
        job
    )

    skills_text = (
        ", ".join(relevant_skills)
        if relevant_skills
        else "my technical skills and academic experience"
    )

    cover_letter = f"""
Dear Hiring Team,

I am writing to express my interest in the {job_title}
position at {company}.

My academic background and technical experience have helped
me develop skills relevant to this opportunity, particularly
in {skills_text}.

I am interested in this internship because it provides an
opportunity to apply my existing knowledge to practical
projects while continuing to develop my technical and
problem-solving abilities.

I would be grateful for the opportunity to contribute to
{company} and learn from the team.

Thank you for considering my application.

Sincerely,
{student_name}
"""

    return cover_letter.strip()


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
        "education": "B.Tech in Artificial Intelligence and Data Science",
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

    customized_resume = customize_resume(
        student,
        job
    )

    cover_letter = generate_cover_letter(
        student,
        job
    )

    print("\n========== CUSTOMIZED RESUME ==========\n")

    for key, value in customized_resume.items():
        print(f"{key}: {value}")

    print("\n========== COVER LETTER ==========\n")
    print(cover_letter)