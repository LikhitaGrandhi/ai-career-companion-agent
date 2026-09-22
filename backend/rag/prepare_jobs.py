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

    # Remove empty rows
    df = df.dropna(how="all")

    # Remove duplicate job postings
    df = df.drop_duplicates(
        subset=[
            "job_title",
            "company",
            "location",
            "description",
            "responsibilities"
        ]
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
# CREATE JOB DOCUMENTS
# =========================================================

def create_job_documents(df):

    documents = []

    for _, row in df.iterrows():

        text = f"""
Job Title:
{row['job_title']}

Company:
{row['company']}

Location:
{row['location']}

Description:
{row['description']}

Responsibilities:
{row['responsibilities']}

Required Skills:
{row['required_skills']}

Preferred Skills:
{row['preferred_skills']}

Qualifications:
{row['qualifications']}

Experience:
{row['experience']}

Education:
{row['education']}
""".strip()

        documents.append({

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

            "education": row["education"],

            "text": text

        })

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
    print("JOB DATA PREPARATION")
    print("===================================")

    print(
        "Total jobs:",
        len(jobs_df)
    )

    print(
        "Documents:",
        len(documents)
    )

    print("\nSample document:\n")

    print(
        documents[0]["text"]
    )