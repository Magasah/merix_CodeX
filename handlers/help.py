"""Обработчик раздела "Помощь" с мультиязычной поддержкой"""
from aiogram import Router, F, types
from translations import get_text
import database as db
import config

router = Router()

@router.message(F.text.in_(["🆘 Помощь", "🆘 Help", "🆘 Yordam", "🆘 Кӯмак"]))
async def show_help(message: types.Message):
    user_lang = db.get_user_language(message.from_user.id) or 'ru'
    db.update_last_interaction(message.from_user.id)
    admin_link = f'<a href="tg://user?id={config.ADMIN_ID}">Связаться с менеджером</a>'
    await message.answer(text=get_text(user_lang, 'help_text', admin_link=admin_link),
                        parse_mode="HTML", disable_web_page_preview=True)
