# -*- coding: utf-8 -*-
"""
Главный файл для запуска Telegram-бота.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher

# Импортируем токен из нашего конфига
from app.config import BOT_TOKEN
from app.db.engine import init_db
from app.handlers import user_handlers, admin_handlers

# Настраиваем логирование для вывода информации в консоль
logging.basicConfig(level=logging.INFO)

async def main():
    """вот
    Основная функция, которая запускает бота.
    """
    # Проверяем, что токен был загружен
    if not BOT_TOKEN:
        logging.error("Ошибка: BOT_TOKEN не найден. Проверьте ваш .env файл.")
        return

    # Инициализируем базу данных и создаем таблицы, если их нета
    logging.info("Инициализация базы данных...")
    init_db()
    logging.info("База данных успешно инициализирована.")

    # Создаем объекты бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Подключаем роутер с нашими обработчиками
    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)

    # Запускаем бота
    logging.info(f"Запуск бота @{(await bot.get_me()).username}...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logging.info("Бот остановлен.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")