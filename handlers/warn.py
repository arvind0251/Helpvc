# handlers/warn.py
from pyrogram import filters
from pyrogram.types import Message
from collections import defaultdict

warn_db = defaultdict(lambda: defaultdict(int))  # warn_db[chat_id][user_id] = warn_count

def warn_handler(app):
    @app.on_message(filters.command("warn") & filters.group)
    async def warn_user(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("Reply to a user's message to warn them.")

        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id

        warn_db[chat_id][user_id] += 1
        count = warn_db[chat_id][user_id]

        if count >= 3:
            try:
                await client.restrict_chat_member(
                    chat_id,
                    user_id,
                    permissions=None
                )
                warn_db[chat_id][user_id] = 0
                await message.reply(
                    f"User has been warned 3 times and is now **muted**."
                )
            except Exception as e:
                await message.reply(f"Failed to mute user: {e}")
        else:
            await message.reply(f"User warned. ({count}/3)")

    @app.on_message(filters.command("unwarn") & filters.group)
    async def unwarn_user(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("Reply to a user's message to unwarn them.")

        user_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id

        if warn_db[chat_id][user_id] > 0:
            warn_db[chat_id][user_id] -= 1
            await message.reply(f"User's warn count decreased to {warn_db[chat_id][user_id]}")
        else:
            await message.reply("User has no active warns.")
