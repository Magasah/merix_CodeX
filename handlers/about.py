"""Обработчик раздела "О компании" с мультиязычной поддержкой"""
from aiogram import Router, F, types
from translations import get_text
import database as db

router = Router()

@router.message(F.text.in_(["ℹ️ О компании", "ℹ️ About Us", "ℹ️ Biz haqimizda", "ℹ️ Дар бораи мо"]))
async def show_about(message: types.Message):
    user_lang = db.get_user_language(message.from_user.id) or 'ru'
    db.update_last_interaction(message.from_user.id)
    await message.answer(text=get_text(user_lang, 'about_text'), parse_mode="HTML")
