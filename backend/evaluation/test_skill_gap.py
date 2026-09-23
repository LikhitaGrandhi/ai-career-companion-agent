from backend.agents.skill_gap_agent import analyze_skill_gap


def evaluate_profile(profile_name, student, job):
    print("\n" + "=" * 50)
    print(profile_name)
    print("=" * 50)

    analysis = analyze_skill_gap(student, job)

    print(f"\nJob: {analysis['job_title']}")
    print(f"Company: {analysis['company']}")

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

    print("\nRecommendations:")
    for recommendation in analysis["recommendations"]:
        print(f"- {recommendation}")

    return analysis


if __name__ == "__main__":

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

    # Profile 1
    student_1 = {
        "skills": [
            "Python",
            "Pandas",
            "Machine Learning"
        ]
    }

    # Profile 2
    student_2 = {
        "skills": [
            "Python",
            "NumPy",
            "Pandas",
            "Scikit-learn",
            "Machine Learning"
        ]
    }

    # Profile 3
    student_3 = {
        "skills": [
            "Python",
            "Java",
            "SQL"
        ]
    }

    results = []

    results.append(
        evaluate_profile(
            "PROFILE 1 — Partial ML Skills",
            student_1,
            job
        )
    )

    results.append(
        evaluate_profile(
            "PROFILE 2 — Strong ML Skills",
            student_2,
            job
        )
    )

    results.append(
        evaluate_profile(
            "PROFILE 3 — Different Technical Background",
            student_3,
            job
        )
    )

    print("\n" + "=" * 50)
    print("M3.1 EVALUATION SUMMARY")
    print("=" * 50)

    for index, result in enumerate(results, start=1):
        print(
            f"Profile {index}: "
            f"{result['required_skill_match_percentage']}% "
            f"required skill match"
        )

    print("\nM3.1 Skill Gap Evaluation Completed")