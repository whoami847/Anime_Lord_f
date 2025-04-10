from pymongo import MongoClient
from config.config import MONGO_DB_URI

client = MongoClient(MONGO_DB_URI)
db = client.anime_lord

def init_db():
    db.users.create_index("user_id", unique=True)

def add_user(user_id: int):
    if not db.users.find_one({"user_id": user_id}):
        db.users.insert_one({"user_id": user_id})

def total_users():
    return db.users.count_documents({})
