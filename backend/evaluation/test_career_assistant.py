from backend.agents.career_assistant import career_assistant


def evaluate_career_assistant(student, job):

    test_queries = {
        "What skills am I missing?": "skill_gap",
        "Help me customize my resume": "resume",
        "Write a cover letter": "cover_letter",
        "Prepare me for the interview": "interview",
        "Tell me about this internship": "job_information",
        "What can you help me with?": "general"
    }

    results = {}

    for query, expected_intent in test_queries.items():

        result = career_assistant(
            student,
            job,
            query
        )

        actual_intent = result["intent"]

        results[query] = {
            "expected": expected_intent,
            "actual": actual_intent,
            "passed": actual_intent == expected_intent
        }

    passed_tests = sum(
        result["passed"]
        for result in results.values()
    )

    total_tests = len(results)

    intent_accuracy = (
        passed_tests / total_tests
    ) * 100

    overall_pass = (
        passed_tests == total_tests
    )

    return {
        "results": results,
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "intent_accuracy": round(
            intent_accuracy,
            2
        ),
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

    evaluation = evaluate_career_assistant(
        student,
        job
    )

    print("\n========== M3.4 EVALUATION ==========\n")

    for query, result in evaluation["results"].items():

        print(f"Query: {query}")
        print(
            f"Expected: {result['expected']}"
        )
        print(
            f"Actual: {result['actual']}"
        )
        print(
            f"Result: "
            f"{'PASS' if result['passed'] else 'FAIL'}"
        )
        print()

    print(
        "Passed Tests:",
        evaluation["passed_tests"]
    )

    print(
        "Total Tests:",
        evaluation["total_tests"]
    )

    print(
        "Intent Accuracy:",
        f"{evaluation['intent_accuracy']}%"
    )

    print(
        "\nOverall M3.4 Result:",
        "PASS" if evaluation["overall_pass"]
        else "FAIL"
    )
    