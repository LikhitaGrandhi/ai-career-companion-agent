from sentence_transformers import SentenceTransformer


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(documents):
    """
    Generate vector embeddings for job documents.
    """

    texts = [doc["text"] for doc in documents]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings


if __name__ == "__main__":
    from prepare_jobs import load_jobs, create_job_documents

    jobs_df = load_jobs()
    documents = create_job_documents(jobs_df)

    embeddings = generate_embeddings(documents)

    print("\nEmbedding generation completed!")
    print("Number of documents:", len(embeddings))
    print("Embedding dimensions:", embeddings.shape[1])