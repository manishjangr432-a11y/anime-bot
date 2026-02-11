import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from config import BOT_TOKEN, ADMIN_ID

# ---------- JSON FUNCTIONS ----------
def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# ---------- START COMMAND ----------
def start(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)

    banned = load_json("banned.json")
    if user_id in banned:
        update.message.reply_text("🚫 You are banned from using this bot.")
        return

    users = load_json("users.json")
    users[user_id] = True
    save_json("users.json", users)

    keyboard = [
        [InlineKeyboardButton("🔥 Action", callback_data="action")],
        [InlineKeyboardButton("❤️ Romance", callback_data="romance")],
        [InlineKeyboardButton("✨ Fantasy", callback_data="fantasy")]
    ]

    update.message.reply_text(
        "👋 Welcome to Anime Discovery Bot!\nChoose a genre:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------- GENRE HANDLER (IMAGE + LINK) ----------
def genre_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    genre = query.data

    if genre == "action":
        image_url = "https://i.imgur.com/2yaf2wb.jpg"
        caption = "🔥 Naruto Shippuden\n\n🎬 Watch Now:\nhttps://example.com"

    elif genre == "romance":
        image_url = "https://i.imgur.com/8KHKhxv.jpg"
        caption = "❤️ Your Name\n\n🎬 Watch Now:\nhttps://example.com"

    elif genre == "fantasy":
        image_url = "https://i.imgur.com/z4d4kWk.jpg"
        caption = "✨ Attack on Titan\n\n🎬 Watch Now:\nhttps://example.com"

    else:
        query.message.reply_text("Anime not found.")
        return

    context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=image_url,
        caption=caption
    )

# ---------- BAN COMMAND (ADMIN ONLY) ----------
def ban(update: Update, context: CallbackContext):
    if update.message.from_user.id != ADMIN_ID:
        return

    if len(context.args) == 0:
        update.message.reply_text("Usage: /ban USER_ID")
        return

    user_id = context.args[0]

    banned = load_json("banned.json")
    banned[user_id] = True
    save_json("banned.json", banned)

    update.message.reply_text("🚫 User banned successfully.")

# ---------- MAIN ----------
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ban", ban))
    dp.add_handler(CallbackQueryHandler(genre_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
