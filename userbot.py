# userbot.py
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from datetime import datetime
from config import API_ID, API_HASH

userapp = Client("userbot", api_id=API_ID, api_hash=API_HASH)

@userapp.on_chat_member_updated()
async def on_vc_join(client: Client, update: ChatMemberUpdated):
    # Trigger when user joins VC (status updated to 'member')
    if (
        update.new_chat_member and
        update.new_chat_member.status == "member" and
        update.old_chat_member.status != "member" and
        update.chat.type in ["supergroup", "group"]
    ):
        user = update.from_user
        chat = update.chat

        msg = (
            "**[Voice Chat Join Detected]**\n\n"
            f"**Name:** {user.first_name or 'No Name'}\n"
            f"**Username:** @{user.username if user.username else 'None'}\n"
            f"**User ID:** `{user.id}`\n"
            f"**Group:** {chat.title}\n"
            f"**Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
        )

        try:
            await userapp.send_message(chat.id, msg)
        except Exception as e:
            print(f"Failed to send message to group: {e}")

if __name__ == "__main__":
    print("Userbot is monitoring VC joins in groups...")
    userapp.run()
