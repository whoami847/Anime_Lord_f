from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config.config import ADMINS, FORCE_SUB
from bot.utils import to_small_caps
from bot.database import add_user, total_users
import asyncio
import time

# /start command
@Client.on_message(filters.command("start"))
async def start(client, message: Message):
    user_id = message.from_user.id
    add_user(user_id)

    # Force Subscribe check
    if FORCE_SUB:
        try:
            member = await client.get_chat_member(FORCE_SUB, user_id)
            if member.status not in ("member", "administrator", "creator"):
                raise Exception()
        except Exception:
            return await message.reply_photo(
                "bot/welcome.jpg",
                caption="**Jᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ!**",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Jᴏɪɴ Nᴏᴡ", url=f"https://t.me/{FORCE_SUB}")],
                    [InlineKeyboardButton("Rᴇꜰʀᴇꜱʜ", callback_data="refresh_start")]
                ])
            )

    # Welcome message with Help & About buttons
    await message.reply_photo(
        "bot/welcome.jpg",
        caption=to_small_caps("Hello, Welcome to Anime Lord Bot!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Hᴇʟᴘ", callback_data="help_cb")],
            [InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about_cb")]
        ])
    )

# Refresh after joining
@Client.on_callback_query(filters.regex("refresh_start"))
async def refresh_start(client, callback_query):
    await start(client, callback_query.message)

# /help
@Client.on_callback_query(filters.regex("help_cb"))
async def help_callback(client, callback_query):
    await callback_query.message.edit_text(
        to_small_caps("Use /genlink to get a sharable link.\nUse /batch to link multiple files."),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start_back")]])
    )

# /about
@Client.on_callback_query(filters.regex("about_cb"))
async def about_callback(client, callback_query):
    await callback_query.message.edit_text(
        to_small_caps("Anime Lord Bot\nBuilt with Pyrogram + MongoDB"),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start_back")]])
    )

# Back button
@Client.on_callback_query(filters.regex("start_back"))
async def back_to_start(client, callback_query):
    await start(client, callback_query.message)

# /genlink
@Client.on_message(filters.command("genlink"))
async def genlink_handler(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply("Reply to a file to generate a link.")
    file = message.reply_to_message.document
    await message.reply(f"Generated link for **{file.file_name}**:\nhttps://t.me/{client.me.username}?start=file_{file.file_id}")

# /batch (Dummy example)
@Client.on_message(filters.command("batch"))
async def batch_handler(client, message: Message):
    await message.reply("Batch processing is under development.")

# /forcesub
@Client.on_message(filters.command("forcesub") & filters.user(ADMINS))
async def force_sub_handler(client, message: Message):
    await message.reply(f"Current force sub channel: `{FORCE_SUB}`")

# /auto_del
@Client.on_message(filters.command("auto_del") & filters.user(ADMINS))
async def auto_del_handler(client, message: Message):
    await message.reply("Auto-delete interval is 20 minutes by default.")

# /welcome (custom set not implemented fully)
@Client.on_message(filters.command("welcome") & filters.user(ADMINS))
async def welcome_handler(client, message: Message):
    await message.reply("Welcome image and message are pre-set.")

# /status
@Client.on_message(filters.command("status") & filters.user(ADMINS))
async def status_handler(client, message: Message):
    await message.reply(f"Total users: {total_users()}")

# /broadcast
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_handler(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")
    
    users = list(client.db.users.find())
    sent = 0
    for user in users:
        try:
            await client.copy_message(chat_id=user["user_id"], from_chat_id=message.chat.id, message_id=message.reply_to_message.id)
            sent += 1
            await asyncio.sleep(0.1)
        except:
            continue
    await message.reply(f"Broadcast sent to {sent} users.")

# /restart
@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_handler(client, message: Message):
    await message.reply("Restarting...")
    time.sleep(2)
    raise SystemExit

# /button-c
custom_buttons = {}

@Client.on_message(filters.command("button-c") & filters.user(ADMINS))
async def button_create_handler(client, message: Message):
    await message.reply("Use /add_button or /remove_button to manage buttons.")

@Client.on_message(filters.command("add_button") & filters.user(ADMINS))
async def add_button(client, message: Message):
    parts = message.text.split(None, 2)
    if len(parts) < 3:
        return await message.reply("Usage: /add_button <name> <url>")
    name, url = parts[1], parts[2]
    custom_buttons[name] = url
    await message.reply(f"Button `{name}` added.")

@Client.on_message(filters.command("remove_button") & filters.user(ADMINS))
async def remove_button(client, message: Message):
    parts = message.text.split(None, 1)
    if len(parts) < 2:
        return await message.reply("Usage: /remove_button <name>")
    name = parts[1]
    if name in custom_buttons:
        del custom_buttons[name]
        await message.reply(f"Button `{name}` removed.")
    else:
        await message.reply("Button not found.")
