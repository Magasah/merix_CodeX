"""
Inline клавиатуры (кнопки под сообщениями)
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translations import get_text


def get_services_keyboard(lang: str = 'ru', page: int = 1) -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора категории услуг с пагинацией"""
    
    # Все услуги
    all_services = [
        InlineKeyboardButton(text=get_text(lang, 'btn_bots'), callback_data="service_bots"),
        InlineKeyboardButton(text=get_text(lang, 'btn_websites'), callback_data="service_websites"),
        InlineKeyboardButton(text=get_text(lang, 'btn_security'), callback_data="service_security"),
        InlineKeyboardButton(text=get_text(lang, 'btn_fast_start'), callback_data="service_package"),
        InlineKeyboardButton(text=get_text(lang, 'btn_ai_automation'), callback_data="service_ai"),
        InlineKeyboardButton(text=get_text(lang, 'btn_tech_support'), callback_data="service_tech"),
        InlineKeyboardButton(text="💻 Скрипты (Игры/Софт)", callback_data="service_scripts"),
        InlineKeyboardButton(text="🎓 Merix Academy", callback_data="merix_academy")
    ]
    
    # Разбиваем на страницы по 4 кнопки
    items_per_page = 4
    total_pages = (len(all_services) + items_per_page - 1) // items_per_page
    
    # Определяем диапазон для текущей страницы
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_services = all_services[start_idx:end_idx]
    
    # Создаем клавиатуру
    keyboard_buttons = [[btn] for btn in current_services]
    
    # Добавляем навигацию если больше одной страницы
    if total_pages > 1:
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"services_page_{page-1}"))
        nav_buttons.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="services_page_info"))
        if page < total_pages:
            nav_buttons.append(InlineKeyboardButton(text="▶️ Далее", callback_data=f"services_page_{page+1}"))
        keyboard_buttons.append(nav_buttons)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
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
            [InlineKeyboardButton(text=get_text(lang, 'btn_broadcast'), callback_data="admin_broadcast")],
            [InlineKeyboardButton(text="✉️ Написать по ID", callback_data="admin_reply_id")]
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


def get_subscription_plans_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с тарифами подписки на Merix Academy"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐️ 7 Дней — 100 Stars", callback_data="sub_7_days")],
            [InlineKeyboardButton(text="⭐️ 14 Дней — 130 Stars", callback_data="sub_14_days")],
            [InlineKeyboardButton(text="⭐️ 30 Дней — 300 Stars", callback_data="sub_30_days")],
            [InlineKeyboardButton(text="💳 Оплата Картой (TJS/RUB)", callback_data="pay_manual")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_services")]
        ]
    )
    return keyboard


def get_payment_approval_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру для подтверждения/отклонения оплаты админом"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"approve_pay_{user_id}")],
            [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_pay_{user_id}")]
        ]
    )
    return keyboard
