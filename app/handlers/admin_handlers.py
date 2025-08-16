# -*- coding: utf-8 -*-
"""
Этот модуль содержит обработчики для админ-панели.
"""

from aiogram import Router, F, types
from aiogram.filters import Command, Filter

from app.config import ADMIN_ID
from app.db.engine import SessionLocal
from app.db.crud import get_users_count, get_all_users

# Создаем роутер для админских обработчиков
router = Router()

# Фильтр для проверки, является ли пользователь администратором
class AdminFilter(Filter):
    async def __call__(self, event: types.Message | types.CallbackQuery) -> bool:
        print(f"Checking user ID: {event.from_user.id}, ADMIN_ID: {ADMIN_ID}")
        return str(event.from_user.id) == ADMIN_ID

@router.message(Command("admin"), AdminFilter())
async def handle_admin_panel(message: types.Message):
    """
    Обработчик команды /admin.
    Показывает основное меню админ-панели.
    """
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Статистика", callback_data="admin_stats")],
        [types.InlineKeyboardButton(text="Пользователи", callback_data="admin_users")]
    ])
    await message.answer("Добро пожаловать в админ-панель!", reply_markup=keyboard)

@router.callback_query(F.data == "admin_stats", AdminFilter())
async def handle_stats(callback_query: types.CallbackQuery):
    """
    Обработчик для кнопки "Статистика".
    Показывает общее количество пользователей.
    """
    db = SessionLocal()
    try:
        count = get_users_count(db)
        await callback_query.message.answer(f"Всего пользователей в боте: {count}")
    finally:
        db.close()
    await callback_query.answer()

@router.callback_query(F.data == "admin_users", AdminFilter())
async def handle_users_list(callback_query: types.CallbackQuery):
    """
    Обработчик для кнопки "Пользователи".
    Показывает список всех пользователей.
    """
    db = SessionLocal()
    try:
        users = get_all_users(db)
        if not users:
            await callback_query.message.answer("Пользователей пока нет.")
            return

        response = "Список пользователей:\n\n"
        for user in users:
            response += f"- {user.full_name} (ID: {user.telegram_id}) - [Профиль](tg://user?id={user.telegram_id})\n"
        
        await callback_query.message.answer(response, parse_mode="Markdown")

    finally:
        db.close()
    await callback_query.answer()
