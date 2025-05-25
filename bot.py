# bot.py
from pyrogram import Client, filters
from datetime import datetime
from config import BOT_TOKEN, API_ID, API_HASH, OWNER_ID, LOG_CHANNEL
from handlers import tagall, admin, welcome

app = Client(
    "helpvc_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=20,
)

# Import handlers
app.add_handler(tagall.tagall_handler)
app.add_handler(admin.admin_handler)
app.add_handler(welcome.welcome_handler)

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start(_, message):
    user = message.from_user
    text = (
        f"Hello, {user.mention}!\n"
        f"Your ID: `{user.id}`\n"
        f"Your Username: @{user.username if user.username else 'None'}\n\n"
        "Use /help to see commands."
    )
    await message.reply_text(text, quote=True)

# Help command
@app.on_message(filters.command("help") & filters.private)
async def help_command(_, message):
    help_text = (
        "**HelpVC Info Bot Commands:**\n\n"
        "/start - Start bot & get your info\n"
        "/help - Show this help message\n"
        "/ping - Check bot response time\n"
        "/tagall - Tag all users in a group (admin only)\n"
        "/ban, /unban, /kick, /mute, /unmute, /warn - Admin tools\n"
    )
    await message.reply_text(help_text, quote=True)

# Ping command
@app.on_message(filters.command("ping") & filters.private)
async def ping(_, message):
    start = datetime.now()
    msg = await message.reply_text("Pinging...")
    end = datetime.now()
    duration = (end - start).microseconds / 1000  # milliseconds
    await msg.edit(f"Pong! Response time: {duration} ms")

if __name__ == "__main__":
    print("HelpVC Info bot is starting...")
    app.run()
