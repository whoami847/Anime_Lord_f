import os

API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "your_mongodb_uri")
FORCE_SUB = os.getenv("FORCE_SUB", "YourChannelUsername")  # without @
ADMINS = list(map(int, os.getenv("ADMINS", "123456789").split()))
