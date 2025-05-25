# userbot.py

from pyrogram import Client, filters
from datetime import datetime
from config import API_ID, API_HASH, OWNER_ID, LOG_CHANNEL, MONGO_URI
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB setup
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["helpvc_bot_db"]

# Create Userbot Client (no bot_token needed)
app = Client(
    "helpvc_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    workers=20,
    in_memory=True
)

# Import handlers
from handlers import tagall, admin, welcome, userbot, antispam

# Register handlers with app
tagall.setup(app, db)
admin.setup(app, db)
welcome.setup(app, db)
userbot.setup(app, db)   # VC notify handler
antispam.setup(app, db)

# Basic /start command
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

# /help command
@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    help_text = (
        "**HelpVC Userbot Commands:**\n\n"
        "/start - Start bot & get your info\n"
        "/help - Show this help message\n"
        "/ping - Check bot response time\n"
        "/tagall - Tag all users in group (admin only)\n"
        "/ban, /unban, /kick, /mute, /unmute, /warn - Admin tools\n\n"
        "Welcome, Anti-Spam, VC Notification system active."
    )
    await message.reply_text(help_text, quote=True)

# /ping command
@app.on_message(filters.command("ping") & filters.private)
async def ping(client, message):
    start = datetime.now()
    msg = await message.reply_text("Pinging...")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await msg.edit(f"Pong! Response time: {duration} ms")

if __name__ == "__main__":
    print("HelpVC Userbot is starting...")
    app.run()
