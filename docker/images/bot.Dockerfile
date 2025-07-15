FROM python:3.12.8-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /service
RUN pip install python-telegram-bot

# Копируем бота
COPY ./services/bot.py /service

# Запускаем бота
CMD ["python", "bot.py"]