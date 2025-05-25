# handlers/admin.py
from pyrogram import filters
from pyrogram.types import Message

def admin_tools(app):
    # /ban command
    @app.on_message(filters.command("ban") & filters.group)
    async def ban_user(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("Reply to a user's message to ban them.")

        try:
            await client.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply("User has been banned.")
        except Exception as e:
            await message.reply(f"Error banning: {e}")

    # /unban command
    @app.on_message(filters.command("unban") & filters.group)
    async def unban_user(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("Reply to a banned user's message to unban them.")

        try:
            await client.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.reply("User has been unbanned.")
        except Exception as e:
            await message.reply(f"Error unbanning: {e}")

    # /mute command
    @app.on_message(filters.command("mute") & filters.group)
    async def mute_user(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("Reply to a user's message to mute them.")

        try:
            await client.restrict_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                permissions=None
            )
            await message.reply("User has been muted.")
        except Exception as e:
            await message.reply(f"Error muting: {e}")

    # /unmute command
    @app.on_message(filters.command("unmute") & filters.group)
    async def unmute_user(client, message: Message):
        if not message.reply_to_message:
            return await message.reply("Reply to muted user's message to unmute them.")

        try:
            await client.restrict_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                permissions={
                    "can_send_messages": True,
                    "can_send_media_messages": True,
                    "can_send_other_messages": True,
                    "can_add_web_page_previews": True,
                }
            )
            await message.reply("User has been unmuted.")
        except Exception as e:
            await message.reply(f"Error unmuting: {e}")
