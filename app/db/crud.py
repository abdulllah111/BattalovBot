# -*- coding: utf-8 -*-
"""
Этот модуль содержит функции для выполнения CRUD-операций (Create, Read, Update, Delete)
с нашими моделями в базе данных.
"""

from sqlalchemy.orm import Session
from . import models

def get_or_create_user(db: Session, telegram_id: int, full_name: str = "") -> models.User:
    """
    Находит пользователя по telegram_id или создает нового, если он не найден.
    
    Args:
        db (Session): Сессия базы данных.
        telegram_id (int): ID пользователя в Telegram.
        full_name (str): Полное имя пользователя (ФИО).
        
    Returns:
        models.User: Объект пользователя (существующий или новый).
    """
    # Пытаемся найти пользователя в базе данных по его telegram_id
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    
    # Если пользователь не найден, создаем нового
    if not user:
        # Создаем новый объект пользователя
        new_user = models.User(telegram_id=telegram_id, full_name=full_name)
        # Добавляем его в сессию
        db.add(new_user)
        # Сохраняем изменения в базе данных
        db.commit()
        # Обновляем объект new_user, чтобы получить данные из БД (например, id и дату)
        db.refresh(new_user)
        return new_user
        
    # Если пользователь найден, но его имя изменилось или было пустым
    if user.full_name != full_name and full_name:
        user.full_name = full_name
        db.commit()
        db.refresh(user)

    return user

def mark_certificate_received(db: Session, telegram_id: int):
    """
    Отмечает, что пользователь получил сертификат.

    Args:
        db (Session): Сессия базы данных.
        telegram_id (int): ID пользователя в Telegram.
    """
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if user:
        user.has_certificate = True
        db.commit()

def get_users_count(db: Session) -> int:
    """
    Возвращает общее количество пользователей в базе данных.

    Args:
        db (Session): Сессия базы данных.

    Returns:
        int: Количество пользователей.
    """
    return db.query(models.User).count()

def get_all_users(db: Session) -> list[models.User]:
    """
    Возвращает список всех пользователей из базы данных.

    Args:
        db (Session): Сессия базы данных.

    Returns:
        list[models.User]: Список пользователей.
    """
    return db.query(models.User).all()
