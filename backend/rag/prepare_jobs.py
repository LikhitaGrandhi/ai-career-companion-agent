import pandas as pd
import os


# =========================================================
# PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "internship_jobs_m2_dataset.csv"
)


# =========================================================
# LOAD JOBS
# =========================================================

def load_jobs():

    df = pd.read_csv(DATA_PATH)

    print("Raw jobs:", len(df))

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate job IDs
    df = df.drop_duplicates(
        subset=["job_id"]
    )

    # Fill missing text values
    text_columns = [
        "job_title",
        "company",
        "location",
        "description",
        "responsibilities",
        "required_skills",
        "preferred_skills",
        "qualifications",
        "experience",
        "education"
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
        )

    print(
        "Unique jobs after duplicate removal:",
        len(df)
    )

    return df


# =========================================================
# CREATE JOB CHUNKS
# =========================================================
def create_job_documents(df):

    documents = []

    for _, row in df.iterrows():

        # -------------------------------------------------
        # Common metadata
        # -------------------------------------------------

        common_metadata = {

            "job_id": row["job_id"],

            "job_title": row["job_title"],

            "company": row["company"],

            "location": row["location"],

            "description": row["description"],

            "responsibilities": row["responsibilities"],

            "required_skills": row["required_skills"],

            "preferred_skills": row["preferred_skills"],

            "qualifications": row["qualifications"],

            "experience": row["experience"],

            "education": row["education"]

        }

        # -------------------------------------------------
        # Chunk 1: Overview
        # -------------------------------------------------

        overview_text = f"""
Job Title:
{row['job_title']}

Company:
{row['company']}

Location:
{row['location']}

Description:
{row['description']}
""".strip()

        overview_chunk = common_metadata.copy()

        overview_chunk["chunk_type"] = "overview"
        overview_chunk["text"] = overview_text

        documents.append(overview_chunk)

        # -------------------------------------------------
        # Chunk 2: Skills
        # -------------------------------------------------

        skills_text = f"""
Job Title:
{row['job_title']}

Required Skills:
{row['required_skills']}

Preferred Skills:
{row['preferred_skills']}
""".strip()

        skills_chunk = common_metadata.copy()

        skills_chunk["chunk_type"] = "skills"
        skills_chunk["text"] = skills_text

        documents.append(skills_chunk)

        # -------------------------------------------------
        # Chunk 3: Responsibilities
        # -------------------------------------------------

        responsibilities_text = f"""
Job Title:
{row['job_title']}

Responsibilities:
{row['responsibilities']}
""".strip()

        responsibilities_chunk = common_metadata.copy()

        responsibilities_chunk["chunk_type"] = "responsibilities"
        responsibilities_chunk["text"] = responsibilities_text

        documents.append(responsibilities_chunk)

        # -------------------------------------------------
        # Chunk 4: Qualifications
        # -------------------------------------------------

        qualifications_text = f"""
Job Title:
{row['job_title']}

Qualifications:
{row['qualifications']}

Experience:
{row['experience']}

Education:
{row['education']}
""".strip()

        qualifications_chunk = common_metadata.copy()

        qualifications_chunk["chunk_type"] = "qualifications"
        qualifications_chunk["text"] = qualifications_text

        documents.append(qualifications_chunk)

    return documents

      


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    jobs_df = load_jobs()

    documents = create_job_documents(
        jobs_df
    )

    print("\n===================================")
    print("JOB CHUNK PREPARATION")
    print("===================================")

    print(
        "Total jobs:",
        len(jobs_df)
    )

    print(
        "Total chunks:",
        len(documents)
    )

    print(
        "Chunks per job:",
        len(documents) // len(jobs_df)
    )

    print("\nSample chunk:\n")

    print(
        documents[0]["text"]
    )