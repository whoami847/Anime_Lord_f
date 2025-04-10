from pyrogram import Client
from bot.config import API_ID, API_HASH, BOT_TOKEN
from bot.all_features import *
from bot.database import init_db
from server import app as flask_app
from threading import Thread

bot = Client(
    name="AnimeLordBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    init_db()
    Thread(target=run_flask).start()
    print("Bot is starting...")
    bot.run()
