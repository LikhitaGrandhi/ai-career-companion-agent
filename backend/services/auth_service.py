from datetime import datetime
from bson import ObjectId
from passlib.context import CryptContext

from backend.database.mongodb import db 
users_collection = db["users"]

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_user(name: str, email: str, password: str):
    existing_user = users_collection.find_one({
        "email": email.lower()
    })

    if existing_user:
        return None

    hashed_password = hash_password(password)

    user = {
        "name": name,
        "email": email.lower(),
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(user)

    return str(result.inserted_id)
def login_user(email: str, password: str):
    user = users_collection.find_one({
        "email": email.lower()
    })

    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    return {
        "user_id": str(user["_id"]),
        "name": user["name"],
        "student_id": user.get("student_id")
    }
