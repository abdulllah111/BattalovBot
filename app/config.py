# -*- coding: utf-8 -*-
"""
Модуль для загрузки конфигурации из переменных окружения.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла, находящегося в корне проекта
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Токен Telegram-бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
# ID администратора
ADMIN_ID = os.getenv("ADMIN_ID")
