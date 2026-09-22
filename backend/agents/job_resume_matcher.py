import re


# =========================================================
# HELPER: CONVERT TEXT TO SKILL SET
# =========================================================

def extract_items(text):
    """
    Convert comma-separated or pipe-separated text
    into a clean set of lowercase items.
    """

    if not text:
        return set()

    text = str(text)

    # Handle comma, pipe and semicolon separated values
    items = re.split(r"[,|;]", text)

    cleaned = set()

    for item in items:
        item = item.strip().lower()

        if item:
            cleaned.add(item)

    return cleaned


# =========================================================
# NORMALIZE SKILL NAMES
# =========================================================

def normalize_skill(skill):

    skill = skill.lower().strip()

    aliases = {
        "ml": "machine learning",
        "ai/ml": "machine learning",
        "scikit learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "js": "javascript",
        "node": "node.js",
        "nodejs": "node.js",
        "reactjs": "react",
        "postgres": "postgresql"
    }

    return aliases.get(skill, skill)


# =========================================================
# NORMALIZE SKILL SET
# =========================================================

def normalize_skills(skills):

    result = set()

    for skill in skills:

        normalized = normalize_skill(skill)

        if normalized:
            result.add(normalized)

    return result


# =========================================================
# GET STUDENT SKILLS
# =========================================================

def get_student_skills(student):

    skills = student.get("skills", [])

    # MongoDB may contain a list
    if isinstance(skills, list):

        return normalize_skills(
            skills
        )

    # Or a string
    return normalize_skills(
        extract_items(skills)
    )


# =========================================================
# GET JOB SKILLS
# =========================================================

def get_job_required_skills(job):

    return normalize_skills(
        extract_items(
            job.get("required_skills", "")
        )
    )


def get_job_preferred_skills(job):

    return normalize_skills(
        extract_items(
            job.get("preferred_skills", "")
        )
    )


# =========================================================
# SKILL MATCHING
# =========================================================

def calculate_skill_match(student_skills, job):

    required_skills = get_job_required_skills(job)

    preferred_skills = get_job_preferred_skills(job)

    if not required_skills:
        required_score = 0
    else:
        matched_required = (
            student_skills &
            required_skills
        )

        required_score = (
            len(matched_required)
            / len(required_skills)
        ) * 100

    if not preferred_skills:
        preferred_score = 0
    else:
        matched_preferred = (
            student_skills &
            preferred_skills
        )

        preferred_score = (
            len(matched_preferred)
            / len(preferred_skills)
        ) * 100

    matched_required = sorted(
        student_skills &
        required_skills
    )

    missing_required = sorted(
        required_skills -
        student_skills
    )

    matched_preferred = sorted(
        student_skills &
        preferred_skills
    )

    return {
        "required_score": round(
            required_score,
            2
        ),

        "preferred_score": round(
            preferred_score,
            2
        ),

        "matched_required_skills":
            matched_required,

        "missing_required_skills":
            missing_required,

        "matched_preferred_skills":
            matched_preferred
    }


# =========================================================
# EDUCATION MATCHING
# =========================================================

def calculate_education_match(student, job):

    student_education = student.get(
        "education",
        []
    )

    job_education = job.get(
        "education",
        ""
    )

    student_text = str(
        student_education
    ).lower()

    job_text = str(
        job_education
    ).lower()

    # Common technical education keywords
    technical_keywords = [
        "b.tech",
        "b.e",
        "b.sc",
        "computer science",
        "information technology",
        "artificial intelligence",
        "data science",
        "engineering"
    ]

    matched = False

    for keyword in technical_keywords:

        if (
            keyword in student_text
            and keyword in job_text
        ):
            matched = True
            break

    # Broader fallback
    if not matched:

        student_keywords = [
            "b.tech",
            "b.e",
            "b.sc",
            "engineering",
            "computer",
            "information technology",
            "artificial intelligence",
            "data science"
        ]

        job_requires_technical = any(
            keyword in job_text
            for keyword in student_keywords
        )

        student_is_technical = any(
            keyword in student_text
            for keyword in student_keywords
        )

        if (
            job_requires_technical
            and student_is_technical
        ):
            matched = True

    return 100 if matched else 50


# =========================================================
# EXPERIENCE MATCHING
# =========================================================

def calculate_experience_match(
    student,
    job
):

    student_experience = student.get(
        "experience",
        []
    )

    job_experience = job.get(
        "experience",
        ""
    )

    student_text = str(
        student_experience
    ).lower()

    job_text = str(
        job_experience
    ).lower()

    # Internship/student profiles generally
    # satisfy 0-1 year internship requirements.
    if (
        "0-1" in job_text
        or "0–1" in job_text
        or "internship" in job_text
        or "student" in job_text
    ):

        if (
            not student_text
            or "internship" in student_text
            or "project" in student_text
            or "academic" in student_text
        ):
            return 100

    # If experience exists, give partial match
    if student_text:
        return 75

    return 50


# =========================================================
# PROJECT RELEVANCE
# =========================================================

def calculate_project_match(
    student,
    job
):

    projects = student.get(
        "projects",
        []
    )

    if not projects:
        return 50

    project_text = str(
        projects
    ).lower()

    job_text = str(
        job.get("text", "")
    ).lower()

    # Check whether important student/project
    # keywords occur in the job description.
    keywords = [
        "python",
        "java",
        "machine learning",
        "data science",
        "react",
        "javascript",
        "mongodb",
        "sql",
        "ai",
        "deep learning",
        "web development"
    ]

    matches = 0

    for keyword in keywords:

        if (
            keyword in project_text
            and keyword in job_text
        ):
            matches += 1

    if matches >= 3:
        return 100

    if matches == 2:
        return 85

    if matches == 1:
        return 70

    return 50


# =========================================================
# CALCULATE OVERALL MATCH SCORE
# =========================================================

def calculate_match_score(
    skill_result,
    education_score,
    experience_score,
    project_score,
    semantic_score
):

    # Weights
    required_skill_weight = 0.40
    preferred_skill_weight = 0.10
    education_weight = 0.15
    experience_weight = 0.10
    project_weight = 0.10
    semantic_weight = 0.15

    score = (

        skill_result["required_score"]
        * required_skill_weight

        +

        skill_result["preferred_score"]
        * preferred_skill_weight

        +

        education_score
        * education_weight

        +

        experience_score
        * experience_weight

        +

        project_score
        * project_weight

        +

        semantic_score
        * semantic_weight
    )

    return round(
        min(score, 100),
        2
    )


# =========================================================
# GENERATE REASONING
# =========================================================

def generate_reasoning(
    student,
    job,
    skill_result,
    education_score,
    experience_score,
    project_score
):

    matched = skill_result[
        "matched_required_skills"
    ]

    missing = skill_result[
        "missing_required_skills"
    ]

    reasoning = []

    # Required skills
    if matched:

        reasoning.append(
            "Matches required skills: "
            + ", ".join(matched)
        )

    if missing:

        reasoning.append(
            "Missing required skills: "
            + ", ".join(missing)
        )

    # Preferred skills
    preferred = skill_result[
        "matched_preferred_skills"
    ]

    if preferred:

        reasoning.append(
            "Also matches preferred skills: "
            + ", ".join(preferred)
        )

    # Education
    if education_score >= 100:

        reasoning.append(
            "Educational background is "
            "aligned with the role."
        )

    else:

        reasoning.append(
            "Education appears partially "
            "aligned with the role."
        )

    # Experience
    if experience_score >= 100:

        reasoning.append(
            "Experience level is suitable "
            "for an internship role."
        )

    # Projects
    if project_score >= 85:

        reasoning.append(
            "Student projects show strong "
            "relevance to the role."
        )

    elif project_score >= 70:

        reasoning.append(
            "Student projects show some "
            "relevance to the role."
        )

    return reasoning


# =========================================================
# MATCH ONE JOB WITH ONE STUDENT
# =========================================================

def match_student_to_job(
    student,
    job,
    semantic_score=0
):

    # ---------------------------------------------
    # Student skills
    # ---------------------------------------------

    student_skills = get_student_skills(
        student
    )

    # ---------------------------------------------
    # Skill matching
    # ---------------------------------------------

    skill_result = calculate_skill_match(
        student_skills,
        job
    )

    # ---------------------------------------------
    # Education
    # ---------------------------------------------

    education_score = calculate_education_match(
        student,
        job
    )

    # ---------------------------------------------
    # Experience
    # ---------------------------------------------

    experience_score = calculate_experience_match(
        student,
        job
    )

    # ---------------------------------------------
    # Projects
    # ---------------------------------------------

    project_score = calculate_project_match(
        student,
        job
    )

    # ---------------------------------------------
    # Semantic score
    # FAISS score is normally 0-1
    # Convert to percentage
    # ---------------------------------------------

    semantic_percentage = (
        float(semantic_score) * 100
    )

    # ---------------------------------------------
    # Overall score
    # ---------------------------------------------

    overall_score = calculate_match_score(
        skill_result,
        education_score,
        experience_score,
        project_score,
        semantic_percentage
    )

    # ---------------------------------------------
    # Reasoning
    # ---------------------------------------------

    reasoning = generate_reasoning(
        student,
        job,
        skill_result,
        education_score,
        experience_score,
        project_score
    )

    # ---------------------------------------------
    # Final result
    # ---------------------------------------------

    return {

        "job_id":
            job.get("job_id"),

        "job_title":
            job.get("job_title"),

        "company":
            job.get("company"),

        "location":
            job.get("location"),

        "match_score":
            overall_score,

        "semantic_similarity":
            round(
                float(semantic_score),
                4
            ),

        "required_skill_score":
            skill_result["required_score"],

        "preferred_skill_score":
            skill_result["preferred_score"],

        "education_score":
            education_score,

        "experience_score":
            experience_score,

        "project_score":
            project_score,

        "matched_required_skills":
            skill_result[
                "matched_required_skills"
            ],

        "missing_required_skills":
            skill_result[
                "missing_required_skills"
            ],

        "matched_preferred_skills":
            skill_result[
                "matched_preferred_skills"
            ],

        "reasoning":
            reasoning
    }


# =========================================================
# MATCH MULTIPLE JOBS
# =========================================================

def match_student_to_jobs(
    student,
    jobs
):

    results = []

    for job in jobs:

        semantic_score = job.get(
            "similarity_score",
            0
        )

        result = match_student_to_job(
            student,
            job,
            semantic_score
        )

        results.append(result)

    # Sort highest match first
    results.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return results