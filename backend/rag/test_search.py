from search_jobs import search_jobs


queries = [
    "Python data science internship",
    "React frontend development internship",
    "Java backend Spring Boot internship"
]


for query in queries:

    print("\n===================================")
    print("QUERY:", query)
    print("===================================")

    results = search_jobs(query, top_k=5)

    for i, job in enumerate(results, start=1):

        print(
            f"{i}. "
            f"{job['job_title']} | "
            f"{job['company']} | "
            f"Score: {job['similarity_score']:.4f}"
        )