"""
Обработчик команды /start с правильной последовательностью:
1. Проверка существования в БД
2. Если нет - выбор языка
3. Проверка подписки на канал
4. Показ главного меню
"""
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.reply import get_main_keyboard
from translations import get_text, LANGUAGE_FLAGS, LANGUAGE_NAMES
import database as db
import config
import logging

logger = logging.getLogger(__name__)

router = Router()


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора языка"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{LANGUAGE_FLAGS['ru']} {LANGUAGE_NAMES['ru']}", 
                callback_data="lang_ru"
            )],
            [InlineKeyboardButton(
                text=f"{LANGUAGE_FLAGS['en']} {LANGUAGE_NAMES['en']}", 
                callback_data="lang_en"
            )],
            [InlineKeyboardButton(
                text=f"{LANGUAGE_FLAGS['tj']} {LANGUAGE_NAMES['tj']}", 
                callback_data="lang_tj"
            )],
            [InlineKeyboardButton(
                text=f"{LANGUAGE_FLAGS['uz']} {LANGUAGE_NAMES['uz']}", 
                callback_data="lang_uz"
            )]
        ]
    )
    return keyboard


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Обработчик /start с правильной последовательностью
    """
    user = message.from_user
    user_id = user.id
    
    # Шаг A: Проверяем существование в БД
    user_lang = db.get_user_language(user_id)
    
    if user_lang is None:
        # Новый пользователь - показываем выбор языка
        logger.info(f"👤 Новый пользователь: {user_id}")
        await message.answer(
            text=get_text('ru', 'choose_language'),
            reply_markup=get_language_keyboard(),
            parse_mode="HTML"
        )
    else:
        # Существующий пользователь - обновляем время взаимодействия
        db.update_last_interaction(user_id)
        
        # Проверяем подписку на канал (middleware уже проверил, но показываем меню)
        await message.answer(
            text=get_text(user_lang, 'welcome', name=user.first_name),
            reply_markup=get_main_keyboard(user_lang),
            parse_mode="HTML"
        )


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    """
    Шаг B: Сохранение выбранного языка
    После сохранения языка middleware автоматически проверит подписку
    """
    lang = callback.data.split("_")[1]
    user = callback.from_user
    
    # Сохраняем пользователя с выбранным языком
    db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        language=lang
    )
    
    logger.info(f"✅ Пользователь {user.id} выбрал язык: {lang}")
    
    # Подтверждение выбора языка
    await callback.message.edit_text(
        text=get_text(lang, 'language_set'),
        parse_mode="HTML"
    )
    
    # Теперь middleware проверит подписку на канал при следующем взаимодействии
    # Показываем приветственное сообщение
    await callback.message.answer(
        text=get_text(lang, 'welcome', name=user.first_name),
        reply_markup=get_main_keyboard(lang),
        parse_mode="HTML"
    )
    
    await callback.answer()
