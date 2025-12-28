"""
Обработчик команды /start с выбором языка
"""
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.reply import get_main_keyboard
from translations import get_text, LANGUAGE_FLAGS, LANGUAGE_NAMES
import database as db

# Создаем роутер для обработчиков команды start
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
    Обработчик команды /start
    Если пользователь новый - показывает выбор языка
    Если существующий - показывает приветствие на его языке
    """
    user = message.from_user
    
    # Обновляем время последнего взаимодействия
    db.update_last_interaction(user.id)
    
    # Проверяем, существует ли пользователь в БД
    user_lang = db.get_user_language(user.id)
    
    if user_lang is None:
        # Новый пользователь - показываем выбор языка
        await message.answer(
            text=get_text('ru', 'choose_language'),
            reply_markup=get_language_keyboard(),
            parse_mode="HTML"
        )
    else:
        # Существующий пользователь - приветствие
        await message.answer(
            text=get_text(user_lang, 'welcome', name=user.first_name),
            reply_markup=get_main_keyboard(user_lang),
            parse_mode="HTML"
        )


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    """
    Обработчик выбора языка
    Сохраняет язык в БД и показывает приветствие
    """
    # Извлекаем код языка из callback_data
    lang = callback.data.split("_")[1]
    user = callback.from_user
    
    # Проверяем, существует ли пользователь
    if db.user_exists(user.id):
        # Обновляем язык
        db.update_user_language(user.id, lang)
    else:
        # Добавляем нового пользователя
        db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            language=lang
        )
    
    # Отправляем уведомление о выборе языка
    await callback.message.edit_text(
        text=get_text(lang, 'language_set'),
        parse_mode="HTML"
    )
    
    # Отправляем приветствие с главным меню
    await callback.message.answer(
        text=get_text(lang, 'welcome', name=user.first_name),
        reply_markup=get_main_keyboard(lang),
        parse_mode="HTML"
    )
    
    await callback.answer()
