
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
# LAZY MODEL LOADING
# ---------------------------------------------------------

model = None


def get_model():
    """Load the embedding model only when first needed."""
    global model

    if model is None:
        model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )

    return model


# ---------------------------------------------------------
# LOAD FAISS INDEX AND JOB METADATA
# ---------------------------------------------------------

index = faiss.read_index(INDEX_PATH)

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

    if not query or not query.strip():
        return []

    # -----------------------------------------------------
    # Convert query into embedding
    # -----------------------------------------------------

    embedding_model = get_model()

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # Normalize query vector
    faiss.normalize_L2(query_embedding)

    # -----------------------------------------------------
    # Retrieve candidate chunks
    # -----------------------------------------------------

    candidate_k = min(
        top_k * 20,
        index.ntotal
    )

    if candidate_k == 0:
        return []

    scores, indices = index.search(
        query_embedding,
        candidate_k
    )

    # -----------------------------------------------------
    # Group chunks by actual job posting
    # -----------------------------------------------------

    job_results = {}

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        if idx >= len(metadata):
            continue

        chunk = metadata[idx]
        similarity_score = float(score)

        # Identify a job using title, company, and location
        job_key = (
            chunk["job_title"].strip().lower(),
            chunk["company"].strip().lower(),
            chunk["location"].strip().lower()
        )

        # First occurrence of this job
        if job_key not in job_results:

            job = chunk.copy()
            job["similarity_score"] = similarity_score
            job["matched_chunk"] = chunk["chunk_type"]

            job_results[job_key] = job

        # Keep the strongest matching chunk
        elif similarity_score > job_results[job_key][
            "similarity_score"
        ]:

            job_results[job_key][
                "similarity_score"
            ] = similarity_score

            job_results[job_key][
                "matched_chunk"
            ] = chunk["chunk_type"]

    # -----------------------------------------------------
    # Sort by similarity and return unique jobs
    # -----------------------------------------------------

    sorted_jobs = sorted(
        job_results.values(),
        key=lambda job: job["similarity_score"],
        reverse=True
    )

    return sorted_jobs[:top_k]


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

    print("\nTotal chunks in vector store:")
    print(index.ntotal)

    print("\nTop Matching Internships:\n")

    results = search_jobs(query, top_k=5)

    for i, job in enumerate(results, start=1):

        print(f"{i}. {job['job_title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(
            f"   Similarity Score: "
            f"{job['similarity_score']:.4f}"
        )
        print(f"   Matched Chunk: {job['matched_chunk']}")
        print(f"   Required Skills: {job.get('required_skills', 'N/A')}")
        print()
