from backend.rag.search_jobs import search_jobs
from backend.agents.job_resume_matcher import match_student_to_jobs


# ==========================================
# M2.4 EVALUATION DATA
# ==========================================

test_profiles = [

    {
        "profile_name": "AI Data Science Student",

        "student": {
            "name": "Test Student 1",

            "skills": [
                "Python",
                "Pandas",
                "NumPy",
                "Machine Learning",
                "SQL"
            ],

            "education": [
                "B.Tech Artificial Intelligence and Data Science"
            ],

            "experience": [],

            "projects": [
                "Machine Learning prediction project using Python",
                "Data analysis project using Pandas and NumPy"
            ],

            "certifications": []
        },

        "query": "Python machine learning data science internship",

        "expected_keywords": [
            "machine learning",
            "data science",
            "python"
        ]
    },


    {
        "profile_name": "Web Development Student",

        "student": {
            "name": "Test Student 2",

            "skills": [
                "HTML",
                "CSS",
                "JavaScript",
                "React",
                "Node.js",
                "MongoDB"
            ],

            "education": [
                "B.Tech Computer Science Engineering"
            ],

            "experience": [],

            "projects": [
                "React web application",
                "MERN stack project"
            ],

            "certifications": []
        },

        "query": "React JavaScript web development internship",

        "expected_keywords": [
            "web",
            "react",
            "javascript"
        ]
    },


    {
        "profile_name": "Java Backend Student",

        "student": {
            "name": "Test Student 3",

            "skills": [
                "Java",
                "SQL",
                "Spring Boot",
                "MongoDB"
            ],

            "education": [
                "B.Tech Computer Science Engineering"
            ],

            "experience": [],

            "projects": [
                "Java Railway Reservation System",
                "Backend application using Java"
            ],

            "certifications": []
        },

        "query": "Java backend software development internship",

        "expected_keywords": [
            "java",
            "software",
            "backend"
        ]
    }
]


# ==========================================
# EVALUATION
# ==========================================

print("\n===================================")
print("M2.4 MATCHING SYSTEM EVALUATION")
print("===================================\n")


total_profiles = len(test_profiles)

retrieval_passes = 0
score_values = []
skill_match_count = 0
reasoning_count = 0


for profile_index, profile in enumerate(test_profiles, start=1):

    print("=" * 60)

    print(f"TEST PROFILE {profile_index}")
    print(f"Profile: {profile['profile_name']}")

    print("\nQuery:")
    print(profile["query"])

    # ------------------------------------------
    # STEP 1: Retrieve jobs
    # ------------------------------------------

    jobs = search_jobs(
        profile["query"],
        top_k=5
    )

    print(f"\nRetrieved jobs: {len(jobs)}")

    # ------------------------------------------
    # STEP 2: Match student against jobs
    # ------------------------------------------

    results = match_student_to_jobs(
        profile["student"],
        jobs
    )

    print("\nTop Matching Jobs:")

    for i, result in enumerate(results, start=1):

        print(
            f"{i}. {result['job_title']} | "
            f"{result['company']} | "
            f"{result['match_score']}%"
        )

    # ------------------------------------------
    # Retrieval evaluation
    # ------------------------------------------

    retrieved_text = " ".join(
        (
            str(job["job_title"]) + " " +
            str(job["description"]) + " " +
            str(job["required_skills"])
        ).lower()
        for job in jobs
    )

    keyword_matches = 0

    for keyword in profile["expected_keywords"]:

        if keyword.lower() in retrieved_text:
            keyword_matches += 1

    retrieval_score = (
        keyword_matches /
        len(profile["expected_keywords"])
    ) * 100

    print(
        f"\nRetrieval relevance: "
        f"{retrieval_score:.2f}%"
    )

    if retrieval_score >= 50:
        retrieval_passes += 1

    # ------------------------------------------
    # Score consistency
    # ------------------------------------------

    for result in results:
        score_values.append(
            result["match_score"]
        )

    # ------------------------------------------
    # Skill matching evaluation
    # ------------------------------------------

    if results:

        top_result = results[0]

        matched_skills = (
            top_result["matched_required_skills"]
        )

        if len(matched_skills) > 0:
            skill_match_count += 1

        # --------------------------------------
        # Reasoning evaluation
        # --------------------------------------

        reasoning = top_result["reasoning"]

        if len(reasoning) > 0:
            reasoning_count += 1

        print("\nTop Job Analysis:")

        print(
            "Matched Skills:",
            ", ".join(matched_skills)
            if matched_skills
            else "None"
        )

        print(
            "Missing Skills:",
            ", ".join(
                top_result["missing_required_skills"]
            )
            if top_result["missing_required_skills"]
            else "None"
        )

        print("\nReasoning:")

        for reason in reasoning:
            print("-", reason)


# ==========================================
# FINAL METRICS
# ==========================================

retrieval_accuracy = (
    retrieval_passes /
    total_profiles
) * 100

skill_matching_accuracy = (
    skill_match_count /
    total_profiles
) * 100

reasoning_success = (
    reasoning_count /
    total_profiles
) * 100

if score_values:

    average_score = (
        sum(score_values) /
        len(score_values)
    )

    score_range = (
        max(score_values) -
        min(score_values)
    )

else:

    average_score = 0
    score_range = 0


# ==========================================
# FINAL REPORT
# ==========================================

print("\n")
print("=" * 60)
print("M2.4 EVALUATION RESULTS")
print("=" * 60)

print(
    f"\nProfiles evaluated: "
    f"{total_profiles}"
)

print(
    f"Retrieval relevance: "
    f"{retrieval_accuracy:.2f}%"
)

print(
    f"Skill matching success: "
    f"{skill_matching_accuracy:.2f}%"
)

print(
    f"Reasoning generation success: "
    f"{reasoning_success:.2f}%"
)

print(
    f"Average match score: "
    f"{average_score:.2f}%"
)

print(
    f"Match score range: "
    f"{score_range:.2f}"
)

print("\n===================================")
print("M2.4 EVALUATION COMPLETED")
print("===================================")