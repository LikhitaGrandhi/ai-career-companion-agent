import re


def extract_items(text):
    """
    Convert comma/semicolon/pipe separated text into a set of
    normalized lowercase items.
    """
    if not text:
        return set()

    items = re.split(r"[,|;]", str(text))

    return {
        item.strip().lower()
        for item in items
        if item.strip()
    }


def normalize_skill(skill):
    """
    Normalize common skill aliases.
    """
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


def normalize_skills(skills):
    """
    Normalize a collection of skills.
    """
    return {
        normalize_skill(skill)
        for skill in skills
        if skill
    }


def get_student_skills(student):
    """
    Extract and normalize student skills.
    """
    skills = student.get("skills", [])

    if isinstance(skills, list):
        return normalize_skills(skills)

    return normalize_skills(extract_items(skills))


def get_job_required_skills(job):
    """
    Extract required skills from a job.
    """
    return normalize_skills(
        extract_items(job.get("required_skills", ""))
    )


def get_job_preferred_skills(job):
    """
    Extract preferred skills from a job.
    """
    return normalize_skills(
        extract_items(job.get("preferred_skills", ""))
    )


def analyze_skill_gap(student, job):
    """
    Compare student skills with internship requirements.
    """

    student_skills = get_student_skills(student)

    required_skills = get_job_required_skills(job)

    preferred_skills = get_job_preferred_skills(job)

    matched_required = student_skills & required_skills

    missing_required = required_skills - student_skills

    matched_preferred = student_skills & preferred_skills

    missing_preferred = preferred_skills - student_skills

    if required_skills:
        required_match_percentage = (
            len(matched_required) /
            len(required_skills)
        ) * 100
    else:
        required_match_percentage = 0

    if preferred_skills:
        preferred_match_percentage = (
            len(matched_preferred) /
            len(preferred_skills)
        ) * 100
    else:
        preferred_match_percentage = 0

    critical_gaps = sorted(missing_required)

    preferred_gaps = sorted(missing_preferred)

    recommendations = []

    for skill in critical_gaps:
        recommendations.append(
            f"Develop skills in {skill} because it is listed as a required skill."
        )

    for skill in preferred_gaps:
        recommendations.append(
            f"Consider learning {skill} to improve alignment with the internship."
        )

    return {
        "job_id": job.get("job_id"),
        "job_title": job.get("job_title"),
        "company": job.get("company"),
        "matched_required_skills": sorted(matched_required),
        "missing_required_skills": sorted(missing_required),
        "matched_preferred_skills": sorted(matched_preferred),
        "missing_preferred_skills": sorted(missing_preferred),
        "required_skill_match_percentage": round(
            required_match_percentage,
            2
        ),
        "preferred_skill_match_percentage": round(
            preferred_match_percentage,
            2
        ),
        "critical_gaps": critical_gaps,
        "preferred_gaps": preferred_gaps,
        "recommendations": recommendations
    }


def generate_skill_gap_summary(analysis):
    """
    Generate a human-readable summary of the skill gap analysis.
    """

    summary = []

    if analysis["matched_required_skills"]:
        summary.append(
            "Matched required skills: "
            + ", ".join(
                analysis["matched_required_skills"]
            )
        )

    if analysis["missing_required_skills"]:
        summary.append(
            "Missing required skills: "
            + ", ".join(
                analysis["missing_required_skills"]
            )
        )

    if analysis["matched_preferred_skills"]:
        summary.append(
            "Matched preferred skills: "
            + ", ".join(
                analysis["matched_preferred_skills"]
            )
        )

    if analysis["missing_preferred_skills"]:
        summary.append(
            "Missing preferred skills: "
            + ", ".join(
                analysis["missing_preferred_skills"]
            )
        )

    return summary


if __name__ == "__main__":

    student = {
        "skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "SQL"
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

    analysis = analyze_skill_gap(
        student,
        job
    )

    summary = generate_skill_gap_summary(
        analysis
    )

    print("\n===================================")
    print("SKILL GAP ANALYSIS AGENT")
    print("===================================")

    print("\nJob:")
    print(
        f"{analysis['job_title']} "
        f"| {analysis['company']}"
    )

    print("\nMatched Required Skills:")
    for skill in analysis["matched_required_skills"]:
        print(f"- {skill}")

    print("\nMissing Required Skills:")
    for skill in analysis["missing_required_skills"]:
        print(f"- {skill}")

    print("\nMatched Preferred Skills:")
    for skill in analysis["matched_preferred_skills"]:
        print(f"- {skill}")

    print("\nMissing Preferred Skills:")
    for skill in analysis["missing_preferred_skills"]:
        print(f"- {skill}")

    print(
        f"\nRequired Skill Match: "
        f"{analysis['required_skill_match_percentage']}%"
    )

    print(
        f"Preferred Skill Match: "
        f"{analysis['preferred_skill_match_percentage']}%"
    )

    print("\nLearning Recommendations:")
    for recommendation in analysis["recommendations"]:
        print(f"- {recommendation}")

    print("\nSummary:")
    for item in summary:
        print(f"- {item}")