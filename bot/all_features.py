from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.config import ADMINS, FORCE_SUB
from bot.database import db
import os

# Start Command Handler
@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    user_id = message.from_user.id

    if FORCE_SUB:
        try:
            member = await client.get_chat_member(FORCE_SUB, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                raise Exception()
        except:
            return await message.reply_text(
                f"**আপনাকে অবশ্যই আমাদের চ্যানেলে জয়েন করতে হবে!**",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("চ্যানেলে যোগ দিন", url=f"https://t.me/{FORCE_SUB}")],
                    [InlineKeyboardButton("✅ জয়েন করেছি", callback_data="checksub")]
                ])
            )

    buttons = await db.get_buttons()
    img_path = "downloads/welcome.jpg"
    caption = f"**স্বাগতম!**\n\nআপনার ইউজার আইডি: `{user_id}`"

    if os.path.exists(img_path):
        await message.reply_photo(
            photo=img_path,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
        )
    else:
        await message.reply_text(
            caption,
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
        )

# ForceSub Check Callback
@Client.on_callback_query(filters.regex("checksub"))
async def check_subscription(client, query: CallbackQuery):
    try:
        member = await client.get_chat_member(FORCE_SUB, query.from_user.id)
        if member.status in ["member", "administrator", "creator"]:
            await query.message.delete()
            await start_command(client, query.message)
        else:
            await query.answer("আগে চ্যানেলে জয়েন করুন!", show_alert=True)
    except:
        await query.answer("আগে চ্যানেলে জয়েন করুন!", show_alert=True)

# Help Command
@Client.on_message(filters.command("help") & filters.private)
async def help_command(client, message: Message):
    await message.reply_text("**সহায়তা:**\n/start - বট চালু করুন\n/help - সাহায্য\n/about - আমাদের সম্পর্কে")

# About Command
@Client.on_message(filters.command("about") & filters.private)
async def about_command(client, message: Message):
    await message.reply_text("**Anime Lord Bot**\nডেভেলপার: @your_username")

# Admins only - Add button
@Client.on_message(filters.command("addbutton") & filters.user(ADMINS))
async def add_button(client, message: Message):
    try:
        _, name, url = message.text.split(None, 2)
        await db.add_button(name, url)
        await message.reply_text(f"✅ বাটন `{name}` যুক্ত হয়েছে।")
    except:
        await message.reply_text("ব্যবহার:\n`/addbutton ButtonName https://example.com`")

# Admins only - Remove button
@Client.on_message(filters.command("removebutton") & filters.user(ADMINS))
async def remove_button(client, message: Message):
    try:
        _, name = message.text.split(None, 1)
        await db.remove_button(name)
        await message.reply_text(f"❌ বাটন `{name}` মুছে ফেলা হয়েছে।")
    except:
        await message.reply_text("ব্যবহার:\n`/removebutton ButtonName`")

# Admins only - Show buttons
@Client.on_message(filters.command("showbuttons") & filters.user(ADMINS))
async def show_buttons(client, message: Message):
    buttons = await db.get_buttons()
    if buttons:
        text = "**বর্তমান বাটনসমূহ:**\n" + "\n".join([f"- {b[0]} -> {b[1]}" for b in buttons])
    else:
        text = "কোনো বাটন সেট করা নেই।"
    await message.reply_text(text)
