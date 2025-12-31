"""
Reply клавиатуры (постоянные кнопки внизу экрана)
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from translations import get_text


def get_main_keyboard(lang: str = 'ru') -> ReplyKeyboardMarkup:
    """
    Создает главную клавиатуру с основными разделами бота
    
    Args:
        lang: Код языка пользователя
        
    Returns:
        ReplyKeyboardMarkup: Главная клавиатура бота
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text(lang, 'btn_services')),
                KeyboardButton(text=get_text(lang, 'btn_profile'))
            ],
            [
                KeyboardButton(text=get_text(lang, 'btn_help')),
                KeyboardButton(text=get_text(lang, 'btn_about'))
            ]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard
