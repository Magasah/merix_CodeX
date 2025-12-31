"""
Обработчик раздела помощи
"""
from aiogram import Router, types, F
from translations import get_text
from keyboards.inline import get_help_keyboard
import database as db

router = Router()


@router.message(F.text.in_([
    "🆘 Помощь",
    "🆘 Help",
    "🆘 Ёрдам",
    "🆘 Кӯмак"
]))
async def show_help(message: types.Message):
    """Показывает раздел помощи с кнопкой менеджера"""
    user_lang = db.get_user_language(message.from_user.id) or 'ru'
    
    await message.answer(
        text=get_text(user_lang, 'help_text'),
        reply_markup=get_help_keyboard(),
        parse_mode="HTML"
    )
