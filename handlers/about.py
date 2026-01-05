"""Обработчик раздела "О компании" с мультиязычной поддержкой"""
from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translations import get_text
import database as db

router = Router()

@router.message(F.text.in_(["ℹ️ О компании", "ℹ️ About Us", "ℹ️ Biz haqimizda", "ℹ️ Дар бораи мо"]))
async def show_about(message: types.Message):
    user_lang = db.get_user_language(message.from_user.id) or 'ru'
    db.update_last_interaction(message.from_user.id)
    
    # Создаем inline-клавиатуру с социальными ссылками
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text(user_lang, 'btn_instagram'),
                    url="https://instagram.com/merix_codex"
                ),
                InlineKeyboardButton(
                    text=get_text(user_lang, 'btn_tiktok'),
                    url="https://www.tiktok.com/@merix_codex?_r=1&_t=ZS-92oyYowf7kv"
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text(user_lang, 'btn_youtube'),
                    url="https://youtube.com/@merix_codex?si=Zy1RvaVFDOSp5fvZ"
                ),
                InlineKeyboardButton(
                    text=get_text(user_lang, 'btn_website'),
                    url="https://merix-codex.netlify.app"
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text(user_lang, 'btn_reviews'),
                    url="https://t.me/otziv_merix_codex"
                )
            ]
        ]
    )
    
    await message.answer(
        text=get_text(user_lang, 'about_text'),
        reply_markup=keyboard,
        parse_mode="HTML"
    )
