from datetime import datetime
from bson import ObjectId

from backend.database.mongodb import db


applications_collection = db["applications"]


# Allowed application statuses
APPLICATION_STATUSES = [
    "Saved",
    "Planning to apply",
    "Applied",
    "Application under review",
    "Shortlisted",
    "Interview scheduled",
    "Interview completed",
    "Offer received",
    "Rejected",
    "Withdrawn",
]


def create_application(student_id: str, application_data: dict):
    """Create a new internship application."""

    application_data["student_id"] = student_id
    application_data["created_at"] = datetime.utcnow()
    application_data["updated_at"] = datetime.utcnow()

    result = applications_collection.insert_one(application_data)

    return str(result.inserted_id)


def get_application(application_id: str, student_id: str):
    """Get one application belonging to a student."""

    application = applications_collection.find_one({
        "_id": ObjectId(application_id),
        "student_id": student_id
    })

    if not application:
        return None

    application["id"] = str(application.pop("_id"))

    return application


def get_student_applications(
    student_id: str,
    status: str = None,
    company: str = None,
    search: str = None
):
    """Get applications belonging to a student with optional filters."""

    query = {
        "student_id": student_id
    }

    if status:
        query["status"] = status

    if company:
        query["company_name"] = {
            "$regex": company,
            "$options": "i"
        }

    if search:
        query["$or"] = [
            {
                "company_name": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "job_title": {
                    "$regex": search,
                    "$options": "i"
                }
            }
        ]

    applications = list(
        applications_collection
        .find(query)
        .sort("created_at", -1)
    )

    for application in applications:
        application["id"] = str(application.pop("_id"))

    return applications


def update_application(
    application_id: str,
    student_id: str,
    update_data: dict
):
    """Update an existing application."""

    update_data["updated_at"] = datetime.utcnow()

    result = applications_collection.update_one(
        {
            "_id": ObjectId(application_id),
            "student_id": student_id
        },
        {
            "$set": update_data
        }
    )

    if result.matched_count == 0:
        return None

    return get_application(application_id, student_id)


def delete_application(
    application_id: str,
    student_id: str
):
    """Delete an application belonging to a student."""

    result = applications_collection.delete_one({
        "_id": ObjectId(application_id),
        "student_id": student_id
    })

    return result.deleted_count > 0


def get_application_dashboard(student_id: str):
    """Return application tracking dashboard statistics."""

    applications = list(
        applications_collection.find({
            "student_id": student_id
        })
    )

    total = len(applications)

    active_statuses = [
        "Saved",
        "Planning to apply",
        "Applied",
        "Application under review",
        "Shortlisted",
        "Interview scheduled",
        "Interview completed",
    ]

    active = sum(
        1
        for app in applications
        if app.get("status") in active_statuses
    )

    interviews = sum(
        1
        for app in applications
        if app.get("status") == "Interview scheduled"
        or app.get("interview_status") == "Scheduled"
    )

    offers = sum(
        1
        for app in applications
        if app.get("status") == "Offer received"
    )

    rejected = sum(
        1
        for app in applications
        if app.get("status") == "Rejected"
    )

    return {
        "total_applications": total,
        "active_applications": active,
        "interviews_scheduled": interviews,
        "offers_received": offers,
        "rejected_applications": rejected,
    }