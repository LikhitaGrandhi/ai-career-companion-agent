import os
import json

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# PATH CONFIGURATION
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

INDEX_PATH = os.path.join(
    BASE_DIR,
    "data",
    "vector_store",
    "jobs.index"
)

METADATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "vector_store",
    "jobs_metadata.json"
)


# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ---------------------------------------------------------
# LOAD FAISS INDEX
# ---------------------------------------------------------

index = faiss.read_index(
    INDEX_PATH
)


# ---------------------------------------------------------
# LOAD JOB METADATA
# ---------------------------------------------------------

with open(
    METADATA_PATH,
    "r",
    encoding="utf-8"
) as file:

    metadata = json.load(file)


# ---------------------------------------------------------
# SEARCH JOBS
# ---------------------------------------------------------

def search_jobs(query, top_k=5):

    # Convert query into embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    # Convert to float32
    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # Normalize query vector
    faiss.normalize_L2(
        query_embedding
    )

    # Search FAISS
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx == -1:
            continue

        job = metadata[idx].copy()

        job["similarity_score"] = float(
            score
        )

        results.append(job)

    return results


# ---------------------------------------------------------
# TEST SEARCH
# ---------------------------------------------------------

if __name__ == "__main__":

    query = (
        "Python machine learning internship "
        "with data science skills"
    )

    print("\n===================================")
    print("SEMANTIC JOB SEARCH")
    print("===================================")

    print("\nSearch Query:")
    print(query)

    print("\nTotal jobs in vector store:")
    print(index.ntotal)

    print("\nTop Matching Internships:\n")

    results = search_jobs(
        query,
        top_k=5
    )

    for i, job in enumerate(
        results,
        start=1
    ):

        print(
            f"{i}. {job['job_title']}"
        )

        print(
            f"   Company: {job['company']}"
        )

        print(
            f"   Location: {job['location']}"
        )

        print(
            f"   Similarity Score: "
            f"{job['similarity_score']:.4f}"
        )

        print(
            f"   Required Skills: "
            f"{job['required_skills']}"
        )

        print()