from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://Anime:Anime@anime.suydbfe.mongodb.net/?retryWrites=true&w=majority&appName=Anime")

client = AsyncIOMotorClient(MONGO_URL)
dbase = client.anime_lord_bot
buttons_collection = dbase.buttons

# Initialize DB
def init_db():
    pass  # MongoDB does not need explicit init

# Add a button
async def add_button(name: str, url: str):
    await buttons_collection.update_one(
        {"name": name},
        {"$set": {"name": name, "url": url}},
        upsert=True
    )

# Remove a button
async def remove_button(name: str):
    await buttons_collection.delete_one({"name": name})

# Get all buttons as InlineKeyboard format
async def get_buttons():
    buttons = []
    async for button in buttons_collection.find({}):
        buttons.append([button["name"], button["url"]])
    return [[dict(text=name, url=url)] for name, url in buttons]
