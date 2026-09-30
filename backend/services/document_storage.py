from datetime import datetime

from backend.database.mongodb import db


documents_collection = db["generated_documents"]


def save_document(
    student_id: str,
    document_type: str,
    job_id: str,
    content
):
    document = {
        "student_id": student_id,
        "document_type": document_type,
        "job_id": job_id,
        "content": content,
        "created_at": datetime.utcnow()
    }

    result = documents_collection.insert_one(document)

    return str(result.inserted_id)


def get_document(document_id: str, student_id: str):
    from bson import ObjectId

    document = documents_collection.find_one({
        "_id": ObjectId(document_id),
        "student_id": student_id
    })

    if not document:
        return None

    document["id"] = str(document.pop("_id"))

    return document