# -*- coding: utf-8 -*-
"""
Этот модуль содержит обработчики для команд и сообщений от пользователя.
"""

import os
import re
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile

from app.db.engine import SessionLocal
from app.db.crud import get_or_create_user, mark_certificate_received
from app.services.image_generator import create_coupon_image

# Создаем роутер для наших обработчиков
router = Router()

# Определяем состояния для нашего диалога
class UserState(StatesGroup):
    awaiting_fio = State() # Состояние ожидания ФИО

def is_valid_fio(fio: str) -> tuple[bool, str]:
    """
    Проверяет корректность введенного ФИО.
    """
    # 1. Проверка на длину
    if not (5 <= len(fio) <= 60):
        return False, "ФИО должно содержать от 5 до 60 символов."

    # 2. Проверка на разрешенные символы (только буквы, пробелы и дефисы)
    if not re.match(r"^[A-Za-zА-Яа-яЁё\s\-]+", fio):
        return False, "ФИО может содержать только буквы, пробелы и дефисы."

    # 3. Проверка на количество слов
    words = fio.split()
    if len(words) != 3:
        return False, "Пожалуйста, введите полное ФИО, состоящее из трех слов (Фамилия Имя Отчество)."

    # 4. Простая эвристическая проверка на "набор букв"
    vowels = "аеёиоуыэюяaeiouy"
    for word in words:
        if not any(char.lower() in vowels for char in word):
            return False, f"Слово '{word}' выглядит некорректно. Пожалуйста, проверьте правильность написания."
        if all(char.lower() in vowels for char in word):
            return False, f"Слово '{word}' выглядит некорректно. Пожалуйста, проверьте правильность написания."

    return True, ""

@router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    """
    Обработчик команды /start.
    Приветствует пользователя, добавляет его в БД и просит ввести ФИО.
    """
    db = SessionLocal()
    try:
        user = get_or_create_user(db, telegram_id=message.from_user.id)
        if user.has_certificate:
            await message.answer("Вы уже получили свой купон.")
            return

        welcome_text = (
            f"Здравствуйте, {message.from_user.full_name}!\n\n"
            f"Чтобы получить купон, напишите свое ФИО:"
        )
        await message.answer(welcome_text)
        await state.set_state(UserState.awaiting_fio)
    finally:
        db.close()

@router.message(UserState.awaiting_fio, F.text)
async def handle_fio(message: types.Message, state: FSMContext):
    """
    Обработчик для состояния awaiting_fio.
    Получает ФИО, генерирует изображение и отправляет его пользователю.
    """
    user_fio = message.text.strip()
    telegram_id = message.from_user.id

    # --- Проверка ФИО ---
    is_valid, error_message = is_valid_fio(user_fio)
    if not is_valid:
        await message.answer(error_message + "\n\nПожалуйста, попробуйте еще раз.")
        return # Оставляем пользователя в том же состоянии

    db = SessionLocal()
    try:
        user = get_or_create_user(db, telegram_id=telegram_id, full_name=user_fio)
        if user.has_certificate:
            await message.answer("Вы уже получили свой купон.")
            return

        await message.answer("Ваш купон готовится...")
        image_path = create_coupon_image(user_fio)

        if image_path and os.path.exists(image_path):
            file_to_send = FSInputFile(image_path)
            await message.answer_photo(file_to_send, caption="Вы можете использовать этот купон на скидку для совершения умры, через компанию Хадж Центр: @hajjcenter✨")
            await message.answer("🎉 Поздравляем! Вы стали участником конкурса от Динислама Батталова — главный приз бесплатная умра! 🕋✨")
            mark_certificate_received(db, telegram_id)
            os.remove(image_path)
        else:
            await message.answer("Произошла ошибка при создании изображения. Пожалуйста, попробуйте еще раз.")

    finally:
        db.close()

    await state.clear()
