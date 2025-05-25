# handlers/tagall.py
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from time import sleep

def tagall_handler(app):
    @app.on_message(filters.command("tagall") & filters.group)
    async def tagall(client, message: Message):
        if not message.from_user:
            return

        # Check if sender is admin
        user_status = await client.get_chat_member(message.chat.id, message.from_user.id)
        if user_status.status not in ("administrator", "creator"):
            return await message.reply("Only admins can use this command.")

        users = []
        async for member in client.get_chat_members(message.chat.id):
            if member.user.is_bot:
                continue
            users.append(member.user)

        # Start tagging in batches
        BATCH_SIZE = 5
        delay = 1.5  # seconds between batches

        await message.reply(f"**Tagging {len(users)} members...**")

        for i in range(0, len(users), BATCH_SIZE):
            batch = users[i:i+BATCH_SIZE]
            text = " ".join([f"[{u.first_name}](tg://user?id={u.id})" for u in batch])
            try:
                await client.send_message(message.chat.id, text, reply_to_message_id=message.id)
            except Exception as e:
                print(f"Error sending tag batch: {e}")
                continue
            sleep(delay)
