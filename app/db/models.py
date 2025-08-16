# -*- coding: utf-8 -*-
"""
Этот модуль определяет модели данных (таблицы) для нашей базы данных.
"""

import datetime
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Создаем базовый класс для наших моделей. Все модели будут наследоваться от него.
Base = declarative_base()

class User(Base):
    """
    Модель для хранения информации о пользователе.
    """
    __tablename__ = "users"

    # Уникальный идентификатор записи в таблице
    id = Column(Integer, primary_key=True, index=True)
    
    # ID пользователя в Telegram. Используем BigInteger, так как ID могут быть большими.
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    
    # Полное имя пользователя (ФИО)
    full_name = Column(String, nullable=False)
    
    # Дата и время первого взаимодействия с ботом. 
    # default=datetime.datetime.utcnow устанавливает значение по умолчанию 
    # на момент создания записи.
    first_interaction_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Флаг, показывающий, получил ли пользователь сертификат
    has_certificate = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, full_name='{self.full_name}', has_certificate={self.has_certificate})>"
