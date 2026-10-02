import os
import json

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

from prepare_jobs import (
    load_jobs,
    create_job_documents
)


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

VECTOR_STORE_DIR = os.path.join(
    BASE_DIR,
    "data",
    "vector_store"
)

INDEX_PATH = os.path.join(
    VECTOR_STORE_DIR,
    "jobs.index"
)

METADATA_PATH = os.path.join(
    VECTOR_STORE_DIR,
    "jobs_metadata.json"
)


# =========================================================
# CREATE VECTOR STORE DIRECTORY
# =========================================================

os.makedirs(
    VECTOR_STORE_DIR,
    exist_ok=True
)


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =========================================================
# LOAD JOB DATA
# =========================================================

jobs_df = load_jobs()


# =========================================================
# CREATE MEANINGFUL JOB CHUNKS
# =========================================================

documents = create_job_documents(
    jobs_df
)

print("\n===================================")
print("BUILDING VECTOR STORE")
print("===================================")

print(
    "Total jobs:",
    len(jobs_df)
)

print(
    "Total chunks:",
    len(documents)
)


# =========================================================
# PREPARE TEXT FOR EMBEDDING
# =========================================================

texts = [
    document["text"]
    for document in documents
]


# =========================================================
# GENERATE EMBEDDINGS
# =========================================================

print("\nGenerating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)


# =========================================================
# CONVERT TO FLOAT32
# =========================================================

embeddings = np.asarray(
    embeddings,
    dtype="float32"
)


# =========================================================
# NORMALIZE EMBEDDINGS
# =========================================================

faiss.normalize_L2(
    embeddings
)


# =========================================================
# CREATE FAISS INDEX
# =========================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(
    dimension
)


# =========================================================
# ADD EMBEDDINGS
# =========================================================

index.add(
    embeddings
)


# =========================================================
# SAVE FAISS INDEX
# =========================================================

faiss.write_index(
    index,
    INDEX_PATH
)


# =========================================================
# SAVE METADATA
# =========================================================

with open(
    METADATA_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        documents,
        file,
        indent=2,
        ensure_ascii=False
    )


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n===================================")
print("VECTOR STORE CREATED SUCCESSFULLY")
print("===================================")

print(
    "Total jobs:",
    len(jobs_df)
)

print(
    "Total chunks indexed:",
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