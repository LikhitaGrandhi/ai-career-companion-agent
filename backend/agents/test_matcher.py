from backend.agents.job_resume_matcher import match_student_to_jobs
from backend.rag.search_jobs import search_jobs

# =========================================================
# SAMPLE STUDENT PROFILE
# =========================================================

student = {
    "name": "Likhita Grandhi",

    "skills": [
        "Python",
        "Java",
        "Machine Learning",
        "Pandas",
        "SQL",
        "HTML",
        "CSS"
    ],

    "education": [
        "B.Tech Artificial Intelligence and Data Science"
    ],

    "experience": [],

    "projects": [
        "AI Resume Analyzer using Python and Machine Learning",
        "Railway Reservation System using Java",
        "BlueGuard Environmental Reporting Platform"
    ],

    "certifications": []
}


# =========================================================
# SEARCH FOR RELEVANT JOBS
# =========================================================

query = """
Python machine learning data science internship
for an AI and Data Science student
"""

print("\n===================================")
print("JOB-RESUME MATCHING AGENT")
print("===================================")

print("\nSearching relevant internships...")

jobs = search_jobs(
    query,
    top_k=5
)

print(
    "Retrieved jobs:",
    len(jobs)
)


# =========================================================
# MATCH STUDENT WITH JOBS
# =========================================================

results = match_student_to_jobs(
    student,
    jobs
)


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n===================================")
print("MATCHED INTERNSHIPS")
print("===================================\n")


for i, result in enumerate(
    results,
    start=1
):

    print(
        f"{i}. {result['job_title']}"
    )

    print(
        f"   Company: {result['company']}"
    )

    print(
        f"   Location: {result['location']}"
    )

    print(
        f"   Overall Match: "
        f"{result['match_score']}%"
    )

    print(
        f"   Semantic Similarity: "
        f"{result['semantic_similarity']}"
    )

    print(
        f"   Required Skill Score: "
        f"{result['required_skill_score']}%"
    )

    print(
        f"   Preferred Skill Score: "
        f"{result['preferred_skill_score']}%"
    )

    print(
        f"   Education Score: "
        f"{result['education_score']}%"
    )

    print(
        f"   Experience Score: "
        f"{result['experience_score']}%"
    )

    print(
        f"   Project Score: "
        f"{result['project_score']}%"
    )

    print(
        "\n   Matched Required Skills:"
    )

    print(
        "   ",
        ", ".join(
            result["matched_required_skills"]
        )
        if result["matched_required_skills"]
        else "None"
    )

    print(
        "\n   Missing Required Skills:"
    )

    print(
        "   ",
        ", ".join(
            result["missing_required_skills"]
        )
        if result["missing_required_skills"]
        else "None"
    )

    print(
        "\n   Reasoning:"
    )

    for reason in result["reasoning"]:

        print(
            "   -",
            reason
        )

    print("\n" + "-" * 60)