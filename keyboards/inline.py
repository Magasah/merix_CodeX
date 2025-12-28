"""
Inline клавиатуры (кнопки под сообщениями)
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translations import get_text


def get_services_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора категории услуг"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, 'btn_bots'), callback_data="service_bots")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_websites'), callback_data="service_websites")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_security'), callback_data="service_security")]
        ]
    )
    return keyboard


def get_service_detail_keyboard(service_type: str, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Создает клавиатуру для детального просмотра услуги"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, 'btn_order'), callback_data=f"order_{service_type}")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_back'), callback_data="back_to_services")]
        ]
    )
    return keyboard


def get_order_confirmation_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Создает клавиатуру подтверждения заказа"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_text(lang, 'btn_send'), callback_data="confirm_order"),
                InlineKeyboardButton(text=get_text(lang, 'btn_cancel'), callback_data="cancel_order")
            ]
        ]
    )
    return keyboard


def get_admin_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Создает клавиатуру админ-панели"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, 'btn_statistics'), callback_data="admin_stats")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_broadcast'), callback_data="admin_broadcast")]
        ]
    )
    return keyboard
