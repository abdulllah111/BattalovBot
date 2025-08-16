# -*- coding: utf-8 -*-
"""
Этот модуль отвечает за настройку подключения к базе данных.
Мы используем SQLAlchemy для работы с БД SQLite.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Путь к файлу нашей базы данных SQLite
DATABASE_URL = "sqlite:///./battalov_bot.db"

# Создаем "движок" SQLAlchemy для подключения к БД
# check_same_thread=False требуется для работы с SQLite в асинхронных
# приложениях, таких как aiogram
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаем класс SessionLocal, экземпляры которого будут сессиями для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Инициализирует базу данных и создает все таблицы, 
    определенные в моделях.
    """
    # Base.metadata.create_all создает таблицы, которые наследуются от Base
    Base.metadata.create_all(bind=engine)
