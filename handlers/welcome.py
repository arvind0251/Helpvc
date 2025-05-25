# handlers/welcome.py
from pyrogram import filters
from pyrogram.types import Message
from tinydb import TinyDB, Query

db = TinyDB("data/welcome.json")
WEL = Query()

def welcome_handler(app):
    @app.on_message(filters.new_chat_members)
    async def welcome(client, message: Message):
        chat_id = str(message.chat.id)
        entry = db.get(WEL.chat_id == chat_id)

        welcome_text = entry["text"] if entry else "Welcome {mention} to {chat}!"

        for user in message.new_chat_members:
            try:
                await message.reply(welcome_text.format(
                    mention=user.mention,
                    chat=message.chat.title
                ))
            except: pass

    @app.on_message(filters.command("setwelcome") & filters.group)
    async def set_welcome(client, message: Message):
        if not message.from_user or not message.from_user.id:
            return

        if not message.from_user.id in (await app.get_chat_member(message.chat.id, message.from_user.id)).privileges:
            return await message.reply("Only admins can set welcome messages.")

        text = message.text.split(None, 1)
        if len(text) < 2:
            return await message.reply("Usage:\n`/setwelcome Welcome {mention} to {chat}`", quote=True)

        db.upsert({"chat_id": str(message.chat.id), "text": text[1]}, WEL.chat_id == str(message.chat.id))
        await message.reply("✅ Custom welcome message has been set.")

    @app.on_message(filters.command("getwelcome") & filters.group)
    async def get_welcome(client, message: Message):
        entry = db.get(WEL.chat_id == str(message.chat.id))
        if not entry:
            return await message.reply("No custom welcome message set.")

        await message.reply(f"Current welcome message:\n\n{entry['text']}")
