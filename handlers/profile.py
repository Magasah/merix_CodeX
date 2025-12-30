"""
Обработчик профиля пользователя с реферальной программой
"""
from aiogram import Router, types, F
from translations import get_text
import database as db
import logging

logger = logging.getLogger(__name__)

# Создаем роутер для обработчиков профиля
router = Router()


@router.message(F.text.in_([
    "👤 Профиль", 
    "👤 Profile", 
    "👤 Профил", 
    "👤 Profil"
]))
async def show_profile(message: types.Message):
    """
    Показывает профиль пользователя с реферальной ссылкой
    """
    user = message.from_user
    
    # Получаем язык пользователя
    user_lang = db.get_user_language(user.id)
    if not user_lang:
        user_lang = 'ru'
    
    # Получаем информацию о пользователе
    user_info = db.get_user_info(user.id)
    
    # Получаем username бота из message
    bot_info = await message.bot.get_me()
    bot_username = bot_info.username
    
    # Формируем реферальную ссылку
    referral_link = f"https://t.me/{bot_username}?start={user.id}"
    
    # Получаем баланс (по умолчанию 0, если нет в БД)
    balance = user_info.get('balance', 0) if user_info else 0
    
    # Формируем текст профиля
    profile_text = get_text(
        user_lang, 
        'profile_text',
        name=user.first_name or "Пользователь",
        username=f"@{user.username}" if user.username else "не указан",
        user_id=user.id,
        balance=balance,
        referral_link=referral_link
    )
    
    await message.answer(
        text=profile_text,
        parse_mode="HTML"
    )
    
    logger.info(f"👤 Пользователь {user.id} просмотрел профиль")
