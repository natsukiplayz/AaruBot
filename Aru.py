import os
import asyncio

from pymongo import MongoClient
from mistralai import Mistral

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.constants import (
    ParseMode,
    ChatType,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==========================
# CONFIG
# ==========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI") 

OD1 = 8752939430
OD2 = 6462525689

SUPPORT_LINK = "https://t.me/AaruSupport"
UPDATES_LINK = "https://t.me/IgAaruu"
GROUP_LINK = "https://t.me/Uchiha_ClaniX"

DEVELOPER_USERNAME = "ig_yuuki"
SUPPORT_USERNAME = "Ig_Jinn"

# ==========================
# MONGODB
# ==========================

client = MongoClient(MONGO_URI)

db = client["aaru_bot"]

users_db = db["users"]
games_db = db["games"]
settings_db = db["settings"]

# ==========================================================
# START COMMAND
# ==========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    users_db.update_one(
        {"user_id": user.id},
        {
            "$set": {
                "first_name": user.first_name,
                "username": user.username
            }
        },
        upsert=True
    )

    mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'

    text = f"""
<b>𝐇𝐞𝐥𝐥𝐨, {mention} ✨</b>

𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 <b>𝐀𝐚𝐫𝐮</b>.

𝐄𝐯𝐞𝐫𝐲 𝐠𝐫𝐞𝐚𝐭 𝐜𝐨𝐧𝐯𝐞𝐫𝐬𝐚𝐭𝐢𝐨𝐧 𝐬𝐭𝐚𝐫𝐭𝐬 𝐰𝐢𝐭𝐡 𝐚 𝐬𝐢𝐧𝐠𝐥𝐞 𝐦𝐞𝐬𝐬𝐚𝐠𝐞.
𝐌𝐚𝐲𝐛𝐞 𝐭𝐨𝐝𝐚𝐲'𝐬 𝐢𝐬 𝐲𝐨𝐮𝐫𝐬.

𝐄𝐧𝐣𝐨𝐲 𝐲𝐨𝐮𝐫 𝐬𝐭𝐚𝐲 💜
"""

    keyboard = [
        [
            InlineKeyboardButton("🛠 𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url=f"https://t.me/{SUPPORT_USERNAME}"),
            InlineKeyboardButton("👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url=f"https://t.me/{DEVELOPER_USERNAME}")
        ],
        [
            InlineKeyboardButton("📢 𝐔𝐩𝐝𝐚𝐭𝐞𝐬", url=UPDATES_LINK),
            InlineKeyboardButton("👥 𝐂𝐨𝐦𝐦𝐮𝐧𝐢𝐭𝐲", url=GROUP_LINK)
        ],
        [
            InlineKeyboardButton("✨ 𝐀𝐝𝐝 𝐀𝐚𝐫𝐮", switch_inline_query="")
        ]
    ]

    await update.message.reply_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )


# ==========================================================
# FONT TABLES
# ==========================================================

FONT2 = str.maketrans({
    "A":"𝐀","B":"𝐁","C":"𝐂","D":"𝐃","E":"𝐄","F":"𝐅","G":"𝐆","H":"𝐇","I":"𝐈","J":"𝐉","K":"𝐊","L":"𝐋","M":"𝐌","N":"𝐍","O":"𝐎","P":"𝐏","Q":"𝐐","R":"𝐑","S":"𝐒","T":"𝐓","U":"𝐔","V":"𝐕","W":"𝐖","X":"𝐗","Y":"𝐘","Z":"𝐙",
    "a":"𝐚","b":"𝐛","c":"𝐜","d":"𝐝","e":"𝐞","f":"𝐟","g":"𝐠","h":"𝐡","i":"𝐢","j":"𝐣","k":"𝐤","l":"𝐥","m":"𝐦","n":"𝐧","o":"𝐨","p":"𝐩","q":"𝐪","r":"𝐫","s":"𝐬","t":"𝐭","u":"𝐮","v":"𝐯","w":"𝐰","x":"𝐱","y":"𝐲","z":"𝐳"
})

FONT3 = str.maketrans({
    "A":"ᴀ","B":"ʙ","C":"ᴄ","D":"ᴅ","E":"ᴇ","F":"ғ","G":"ɢ","H":"ʜ","I":"ɪ","J":"ᴊ","K":"ᴋ","L":"ʟ","M":"ᴍ","N":"ɴ","O":"ᴏ","P":"ᴘ","Q":"ǫ","R":"ʀ","S":"s","T":"ᴛ","U":"ᴜ","V":"ᴠ","W":"ᴡ","X":"x","Y":"ʏ","Z":"ᴢ",
    "a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ғ","g":"ɢ","h":"ʜ","i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"ɴ","o":"ᴏ","p":"ᴘ","q":"ǫ","r":"ʀ","s":"s","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x","y":"ʏ","z":"ᴢ"
})


# ==========================================================
# FONT COMMAND
# ==========================================================

async def font(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 1:
        await update.message.reply_text(
            "𝐔𝐬𝐚𝐠𝐞:\n"
            "<code>/f 2 [text]</code>\n"
            "<code>/f 3 [text]</code>\n\n"
            "𝐎𝐫 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐦𝐞𝐬𝐬𝐚𝐠𝐞:\n"
            "<code>/f 2</code>\n"
            "<code>/f 3</code>",
            parse_mode=ParseMode.HTML
        )
        return

    style = context.args[0]

    if style not in ("2", "3"):
        await update.message.reply_text(
            "𝐔𝐬𝐚𝐠𝐞:\n"
            "<code>/f 2 [text]</code>\n"
            "<code>/f 3 [text]</code>",
            parse_mode=ParseMode.HTML
        )
        return

    if update.message.reply_to_message:
        text = (
            update.message.reply_to_message.text
            or update.message.reply_to_message.caption
        )
    else:
        text = " ".join(context.args[1:])

    if not text:
        await update.message.reply_text(
            "𝐔𝐬𝐚𝐠𝐞:\n"
            "<code>/f 2 [text]</code>\n"
            "<code>/f 3 [text]</code>",
            parse_mode=ParseMode.HTML
        )
        return

    if style == "2":
        result = text.translate(FONT2)
    else:
        result = text.translate(FONT3)

    await update.message.reply_text(result)

API_KEY = os.getenv("API_KEY")

client = Mistral(api_key=API_KEY)

# Mongo collection
chat_settings = db["chat_settings"]


# ==========================
# AI
# ==========================

async def ai_chat(user_message: str):

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": """
YOUR PROMPT HERE
(Example: You are Aaru, a friendly girl who chats naturally...)
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.8,
        max_tokens=500
    )

    return response.choices[0].message.content


# ==========================
# /chat
# ==========================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.type == ChatType.PRIVATE:
        await update.message.reply_text(
            "💜 Chat is always enabled in private."
        )
        return

    member = await context.bot.get_chat_member(
        update.effective_chat.id,
        update.effective_user.id
    )

    if member.status not in ("administrator", "creator"):
        await update.message.reply_text(
            "Only admins can change chat mode."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/chat on\n/chat off"
        )
        return

    mode = context.args[0].lower()

    if mode == "on":

        chat_settings.update_one(
            {"chat_id": update.effective_chat.id},
            {"$set": {"enabled": True}},
            upsert=True
        )

        await update.message.reply_text(
            "✨ Chat mode enabled."
        )

    elif mode == "off":

        chat_settings.update_one(
            {"chat_id": update.effective_chat.id},
            {"$set": {"enabled": False}},
            upsert=True
        )

        await update.message.reply_text(
            "✨ Chat mode disabled."
        )

    else:

        await update.message.reply_text(
            "Use /chat on or /chat off."
        )


# ==========================
# AI MESSAGE
# ==========================

async def ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message

    if not message or not message.text:
        return

    # Private → Always ON
    if update.effective_chat.type == ChatType.PRIVATE:
        enabled = True

    else:
        data = chat_settings.find_one(
            {"chat_id": update.effective_chat.id}
        )

        enabled = data.get("enabled", False) if data else False

        if not enabled:
            return

        me = await context.bot.get_me()

        mentioned = (
            message.text
            and f"@{me.username.lower()}" in message.text.lower()
        )

        replied = (
            message.reply_to_message
            and message.reply_to_message.from_user.id == me.id
        )

        if not (mentioned or replied):
            return

    try:

        reply = await ai_chat(message.text)

        await message.reply_text(reply)

    except Exception as e:

        await message.reply_text(
            f"Error:\n{e}"
        )

# ==========================
# MAIN
# ==========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("f", font))
    app.add_handler(CommandHandler("chat", chat))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ai_message
        )
    )

    PORT = int(os.environ.get("PORT", 10000))
    RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

    print("Aaru Bot is running...")

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=f"{RENDER_URL}/{BOT_TOKEN}",
    secret_token=WEBHOOK_SECRET,
)


if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    main()