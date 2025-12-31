"""
Обработчик профиля с настройками и заказами
"""
from aiogram import Router, types, F
from translations import get_text, LANGUAGE_FLAGS, LANGUAGE_NAMES
from keyboards.inline import get_profile_keyboard, get_settings_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import database as db
import logging

logger = logging.getLogger(__name__)

router = Router()


def get_language_selection_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка для настроек"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{LANGUAGE_FLAGS['ru']} {LANGUAGE_NAMES['ru']}", callback_data="changelang_ru")],
            [InlineKeyboardButton(text=f"{LANGUAGE_FLAGS['en']} {LANGUAGE_NAMES['en']}", callback_data="changelang_en")],
            [InlineKeyboardButton(text=f"{LANGUAGE_FLAGS['tj']} {LANGUAGE_NAMES['tj']}", callback_data="changelang_tj")],
            [InlineKeyboardButton(text=f"{LANGUAGE_FLAGS['uz']} {LANGUAGE_NAMES['uz']}", callback_data="changelang_uz")],
            [InlineKeyboardButton(text=get_text('ru', 'btn_back'), callback_data="profile_settings")]
        ]
    )
    return keyboard


@router.message(F.text.in_([
    "👤 Профиль", 
    "👤 Profile", 
    "👤 Профил", 
    "👤 Profil"
]))
async def show_profile(message: types.Message):
    """Показывает профиль пользователя"""
    user = message.from_user
    user_lang = db.get_user_language(user.id) or 'ru'
    
    # Получаем информацию о пользователе
    user_info = db.get_user_info(user.id)
    balance = user_info.get('balance', 0) if user_info else 0
    orders_count = db.get_user_orders_count(user.id)
    
    profile_text = get_text(
        user_lang,
        'profile_text',
        user_id=user.id,
        name=user.first_name or "Пользователь",
        username=f"@{user.username}" if user.username else "не указан",
        balance=balance,
        orders_count=orders_count
    )
    
    await message.answer(
        text=profile_text,
        reply_markup=get_profile_keyboard(user_lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "profile_settings")
async def show_settings(callback: types.CallbackQuery):
    """Показывает настройки профиля"""
    user_lang = db.get_user_language(callback.from_user.id) or 'ru'
    
    await callback.message.edit_text(
        text="⚙️ <b>Настройки профиля</b>\n\nВыберите действие:",
        reply_markup=get_settings_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "change_language")
async def show_language_selection(callback: types.CallbackQuery):
    """Показывает выбор языка"""
    await callback.message.edit_text(
        text="🌐 <b>Выберите язык / Choose language</b>",
        reply_markup=get_language_selection_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("changelang_"))
async def change_user_language(callback: types.CallbackQuery):
    """Изменяет язык пользователя"""
    new_lang = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    db.update_user_language(user_id, new_lang)
    logger.info(f"🌐 Пользователь {user_id} сменил язык на: {new_lang}")
    
    await callback.message.edit_text(
        text=get_text(new_lang, 'language_set'),
        parse_mode="HTML"
    )
    
    # Показываем обновленный профиль
    user_info = db.get_user_info(user_id)
    balance = user_info.get('balance', 0) if user_info else 0
    orders_count = db.get_user_orders_count(user_id)
    
    profile_text = get_text(
        new_lang,
        'profile_text',
        user_id=user_id,
        name=callback.from_user.first_name or "User",
        username=f"@{callback.from_user.username}" if callback.from_user.username else "not set",
        balance=balance,
        orders_count=orders_count
    )
    
    await callback.message.answer(
        text=profile_text,
        reply_markup=get_profile_keyboard(new_lang),
        parse_mode="HTML"
    )
    
    # Импортируем get_main_keyboard и обновляем главное меню
    from keyboards.reply import get_main_keyboard
    
    # Отправляем главное меню с обновленным языком
    await callback.message.answer(
        text=get_text(new_lang, 'menu_updated'),
        reply_markup=get_main_keyboard(new_lang)
    )
    
    await callback.answer()


@router.callback_query(F.data == "back_to_profile")
async def back_to_profile(callback: types.CallbackQuery):
    """Возврат к профилю"""
    user = callback.from_user
    user_lang = db.get_user_language(user.id) or 'ru'
    
    user_info = db.get_user_info(user.id)
    balance = user_info.get('balance', 0) if user_info else 0
    orders_count = db.get_user_orders_count(user.id)
    
    profile_text = get_text(
        user_lang,
        'profile_text',
        user_id=user.id,
        name=user.first_name or "Пользователь",
        username=f"@{user.username}" if user.username else "не указан",
        balance=balance,
        orders_count=orders_count
    )
    
    await callback.message.edit_text(
        text=profile_text,
        reply_markup=get_profile_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "profile_orders")
async def show_user_orders(callback: types.CallbackQuery):
    """Показывает заказы пользователя"""
    user_id = callback.from_user.id
    user_lang = db.get_user_language(user_id) or 'ru'
    
    orders = db.get_user_orders(user_id)
    
    if not orders:
        await callback.message.edit_text(
            text=get_text(user_lang, 'no_orders'),
            parse_mode="HTML"
        )
        await callback.answer()
        return
    
    # Формируем список заказов
    orders_text = get_text(user_lang, 'my_orders_title')
    
    status_map = {
        'Pending': get_text(user_lang, 'order_status_pending'),
        'In Progress': get_text(user_lang, 'order_status_in_progress'),
        'Done': get_text(user_lang, 'order_status_done'),
        'Cancelled': get_text(user_lang, 'order_status_cancelled')
    }
    
    for order in orders:
        order_id, service_name, status, created_at = order
        status_emoji = status_map.get(status, status)
        orders_text += f"📦 <b>Заказ #{order_id}</b>\n"
        orders_text += f"🛠 {service_name}\n"
        orders_text += f"📊 Статус: {status_emoji}\n"
        orders_text += f"📅 {created_at[:10]}\n\n"
    
    # Кнопка возврата
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_lang, 'btn_back'), callback_data="back_to_profile")]
        ]
    )
    
    await callback.message.edit_text(
        text=orders_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()
