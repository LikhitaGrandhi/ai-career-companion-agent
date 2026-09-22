import os
import json
import faiss
import numpy as np

from prepare_jobs import load_jobs, create_job_documents
from embeddings import generate_embeddings


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

INDEX_DIR = os.path.join(
    BASE_DIR,
    "data",
    "vector_store"
)

INDEX_PATH = os.path.join(
    INDEX_DIR,
    "jobs.index"
)

METADATA_PATH = os.path.join(
    INDEX_DIR,
    "jobs_metadata.json"
)


# =========================================================
# BUILD VECTOR STORE
# =========================================================

def build_vector_store():

    print("\n===================================")
    print("BUILDING VECTOR STORE")
    print("===================================")

    # Load cleaned jobs
    jobs_df = load_jobs()

    # Create documents
    documents = create_job_documents(jobs_df)

    print("\nDocuments created:", len(documents))

    # Generate embeddings
    print("\nGenerating embeddings...")

    embeddings = generate_embeddings(documents)

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    # Normalize vectors
    faiss.normalize_L2(embeddings)

    # Embedding dimension
    dimension = embeddings.shape[1]

    # Create FAISS index
    index = faiss.IndexFlatIP(
        dimension
    )

    # Add embeddings
    index.add(embeddings)

    # Create directory
    os.makedirs(
        INDEX_DIR,
        exist_ok=True
    )

    # Save FAISS index
    faiss.write_index(
        index,
        INDEX_PATH
    )

    # -----------------------------------------------------
    # SAVE METADATA
    # -----------------------------------------------------

    metadata = []

    for document in documents:

        metadata.append({
            "job_id": document["job_id"],
            "job_title": document["job_title"],
            "company": document["company"],
            "location": document["location"],
            "description": document["description"],
            "responsibilities": document["responsibilities"],
            "required_skills": document["required_skills"],
            "preferred_skills": document["preferred_skills"],
            "qualifications": document["qualifications"],
            "experience": document["experience"],
            "education": document["education"],
            "text": document["text"]
        })

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4
        )

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    print("\n===================================")
    print("VECTOR STORE CREATED SUCCESSFULLY")
    print("===================================")

    print(
        "Total jobs indexed:",
        index.ntotal
    )

    print(
        "Vector dimensions:",
        dimension
    )

    print(
        "\nFAISS index:",
        INDEX_PATH
    )

    print(
        "Metadata:",
        METADATA_PATH
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    build_vector_store()