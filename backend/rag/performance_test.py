import time
from search_jobs import search_jobs


queries = [
    "Python data science internship",
    "React frontend development internship",
    "Java backend Spring Boot internship"
]

print("\n===== RAG PERFORMANCE TEST =====")

times = []

for query in queries:

    start_time = time.perf_counter()

    results = search_jobs(query, top_k=5)

    end_time = time.perf_counter()

    elapsed = end_time - start_time
    times.append(elapsed)

    print("\nQuery:", query)
    print("Results returned:", len(results))
    print("Retrieval time:", round(elapsed * 1000, 2), "ms")


average_time = sum(times) / len(times)

print("\n==============================")
print(
    "Average retrieval time:",
    round(average_time * 1000, 2),
    "ms"
)
print("==============================")