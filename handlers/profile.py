"""Обработчик раздела "Профиль" с мультиязычной поддержкой"""
from aiogram import Router, F, types
from translations import get_text
import database as db

router = Router()

@router.message(F.text.in_(["👤 Профиль", "👤 Profile", "👤 Profil"]))
async def show_profile(message: types.Message):
    user = message.from_user
    user_lang = db.get_user_language(user.id) or 'ru'
    db.update_last_interaction(user.id)
    username = f"@{user.username}" if user.username else "Не указан"
    await message.answer(text=get_text(user_lang, 'profile_text', 
                                       name=user.full_name, username=username, user_id=user.id), parse_mode="HTML")
