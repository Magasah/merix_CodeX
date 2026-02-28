"""
Обработчик раздела помощи
"""
from aiogram import Router, types, F
from translations import get_text
from keyboards.inline import get_help_keyboard
import database as db
import config

router = Router()


@router.message(F.text.in_([
    "🆘 Помощь",
    "🆘 Help",
    "🆘 Ёрдам",
    "🆘 Кӯмак"
]))
async def show_help(message: types.Message):
    """Показывает раздел помощи с кнопкой администратора"""
    user_lang = db.get_user_language(message.from_user.id) or 'ru'
    admin_link = f'<a href="tg://user?id={config.ADMIN_ID}">🆔 {config.ADMIN_ID}</a>'
    
    await message.answer(
        text=get_text(user_lang, 'help_text', admin_link=admin_link),
        reply_markup=get_help_keyboard(user_lang),
        parse_mode="HTML"
    )
