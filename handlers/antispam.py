# handlers/antispam.py
from pyrogram import filters
from pyrogram.types import Message
import re

BAD_WORDS = ["fuck", "bitch", "chutiya", "nigga", "mc", "bc"]  # customize your list

def antispam_handler(app):
    @app.on_message(filters.text & filters.group)
    async def delete_spam(client, message: Message):
        text = message.text.lower()

        # Delete invite links
        if "t.me/joinchat/" in text or "t.me/" in text and "/+" in text:
            try:
                await message.delete()
            except: pass

        # Delete URLs
        if re.search(r"(http|https)://", text):
            try:
                await message.delete()
            except: pass

        # Delete bad words
        for word in BAD_WORDS:
            if word in text:
                try:
                    await message.delete()
                    await message.reply(f"Don't use bad words, {message.from_user.mention}!")
                    break
                except: pass
