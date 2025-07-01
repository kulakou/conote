from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "7846840591:AAG7Dzdxd3VPBCCeWVUVwgqbNzxcj8FLUac"

WEBAPP_URL = "https://app.conote.app"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Нажми на кнопку около окна ввода сообщения, чтобы открыть CoNote 👇"
    )
    await update.message.reply_text(
        "Приложение также можно открывать прямо из списка чатов по появившейся рядом кнопке!"

    )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
