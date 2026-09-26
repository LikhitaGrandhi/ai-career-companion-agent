import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv("backend/.env")

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "career_companion")

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

students_collection = db["students"]


def test_connection():
    try:
        client.admin.command("ping")
        print("MongoDB connected successfully!")
        return True
    except Exception as e:
        print("MongoDB connection failed:", e)
        return False