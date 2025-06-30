from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Твой токен
BOT_TOKEN = "7846840591:AAG7Dzdxd3VPBCCeWVUVwgqbNzxcj8FLUac"

# URL, на который будет вести WebApp кнопка
WEBAPP_URL = "https://app.conote.app"  # Это и есть твой Mini App


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                text="Открыть CoNote",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! Нажми на кнопку, чтобы открыть CoNote Mini App 👇",
        reply_markup=reply_markup
    )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Бот запущен...")
    app.run_polling()
