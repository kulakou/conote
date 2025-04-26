import asyncio

from logger import logger
from settings import settings
from telebot.async_telebot import AsyncTeleBot

app = AsyncTeleBot(token=settings.api_token)


@app.message_handler(commands=['start'])
async def command_start(message):
    text = 'Welcome'
    await app.reply_to(message, text)


@app.message_handler(commands=['help'])
async def command_help(message):
    text = 'Help'
    await app.reply_to(message, text)


if __name__ == "__main__":
    logger.info("Application polling started")
    asyncio.run(app.infinity_polling())
