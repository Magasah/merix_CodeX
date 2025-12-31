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
            [InlineKeyboardButton(text=get_text(lang, 'btn_security'), callback_data="service_security")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_fast_start'), callback_data="service_fast_start")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_ai_automation'), callback_data="service_ai_automation")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_tech_support'), callback_data="service_tech_support")]
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
            [InlineKeyboardButton(text=get_text(lang, 'btn_active_orders'), callback_data="admin_orders")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_broadcast'), callback_data="admin_broadcast")]
        ]
    )
    return keyboard


def get_profile_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Создает клавиатуру профиля"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, 'btn_settings'), callback_data="profile_settings")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_my_orders'), callback_data="profile_orders")]
        ]
    )
    return keyboard


def get_settings_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """Создает клавиатуру настроек"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, 'btn_change_language'), callback_data="change_language")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_back'), callback_data="back_to_profile")]
        ]
    )
    return keyboard


def get_help_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для раздела помощи"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👨‍💻 Менеджер", url="https://t.me/noxsec")]
        ]
    )
    return keyboard


def get_order_management_keyboard(order_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    """Создает клавиатуру управления заказом для админа"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, 'btn_set_working'), callback_data=f"order_status_{order_id}_In Progress")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_set_done'), callback_data=f"order_status_{order_id}_Done")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_set_cancelled'), callback_data=f"order_status_{order_id}_Cancelled")],
            [InlineKeyboardButton(text=get_text(lang, 'btn_back'), callback_data="admin_orders")]
        ]
    )
    return keyboard
