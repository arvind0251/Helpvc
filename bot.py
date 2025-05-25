from pyrogram import Client, filters
from datetime import datetime
from config import API_ID, API_HASH, OWNER_ID, LOG_CHANNEL

# Create userbot client (no bot_token needed)
app = Client(
    "helpvc_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    workers=20,
)

# Import handlers
from handlers import tagall, admin, welcome, userbot, antispam  # userbot = vc notify handler

# Register handlers
tagall.setup(app)
admin.setup(app)
welcome.setup(app)
userbot.setup(app)  # VC notify handler
antispam.setup(app)

# Basic commands
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user = message.from_user
    text = (
        f"Hello, {user.mention}!\n"
        f"Your ID: `{user.id}`\n"
        f"Your Username: @{user.username if user.username else 'None'}\n\n"
        "Use /help to see commands."
    )
    await message.reply_text(text, quote=True)

@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    help_text = (
        "**HelpVC Userbot Commands:**\n\n"
        "/start - Start bot & get your info\n"
        "/help - Show this help message\n"
        "/ping - Check bot response time\n"
        "/tagall - Tag all users in a group (admin only)\n"
        "/ban, /unban, /kick, /mute, /unmute, /warn - Admin tools\n"
        "Anti-spam, welcome messages & VC notifications active."
    )
    await message.reply_text(help_text, quote=True)

@app.on_message(filters.command("ping") & filters.private)
async def ping(client, message):
    start = datetime.now()
    msg = await message.reply_text("Pinging...")
    end = datetime.now()
    duration = (end - start).microseconds / 1000  # milliseconds
    await msg.edit(f"Pong! Response time: {duration} ms")

if __name__ == "__main__":
    print("HelpVC Userbot is starting...")
    app.run()
