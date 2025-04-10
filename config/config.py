import os

API_ID = int(os.getenv("API_ID", "21463947"))
API_HASH = os.getenv("API_HASH", "39d6a5245f670ee68c507e274b3c7b3d")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7327021662:AAGYxW11fymRBqnDGUUTCLfP9FG0zrv1jKs")
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "your_mongodb_uri")
FORCE_SUB = os.getenv("FORCE_SUB", "log_chana")  # without @
ADMINS = list(map(int, os.getenv("ADMINS", "7282066033").split()))
