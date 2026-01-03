"""
Обработчик админ-панели с управлением заказами
"""
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translations import get_text
from keyboards.inline import get_admin_keyboard, get_order_management_keyboard
from states.order import BroadcastStates, AdminReplyStates
import database as db
import config
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    """Админ-панель (скрыта из меню команд)"""
    user_id = message.from_user.id
    
    if user_id != config.ADMIN_ID:
        await message.answer(text=get_text('ru', 'not_admin'), parse_mode="HTML")
        return
    
    user_lang = db.get_user_language(user_id) or 'ru'
    
    await message.answer(
        text=get_text(user_lang, 'admin_panel'),
        reply_markup=get_admin_keyboard(user_lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin_stats")
async def show_statistics(callback: types.CallbackQuery):
    """Показывает статистику (ИСПРАВЛЕННАЯ ВЕРСИЯ)"""
    user_id = callback.from_user.id
    
    # SECURITY: Проверка прав доступа (только admin)
    if not db.has_permission(user_id, 'admin'):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        logger.warning(f"⚠️ Попытка неавторизованного доступа к статистике: user_id={user_id}")
        return
    
    user_lang = db.get_user_language(callback.from_user.id) or 'ru'
    
    # Получаем статистику из базы данных
    total_users = db.get_users_count()
    vip_users = db.get_vip_users_count()
    current_date = datetime.now().strftime("%d.%m.%Y")
    
    stats_text = (
        f"📊 <b>Статистика Бота:</b>\n\n"
        f"👥 Всего юзеров: {total_users}\n"
        f"💎 VIP подписчиков: {vip_users}\n"
        f"📅 Дата: {current_date}"
    )
    
    # Отправляем НОВОЕ сообщение (не редактируем)
    await callback.message.answer(
        text=stats_text,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_orders")
async def show_active_orders(callback: types.CallbackQuery):
    """Показывает список активных заказов"""
    user_id = callback.from_user.id
    
    # SECURITY: Проверка прав доступа (только admin)
    if not db.has_permission(user_id, 'admin'):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        logger.warning(f"⚠️ Попытка неавторизованного доступа к заказам: user_id={user_id}")
        return
    
    user_lang = db.get_user_language(callback.from_user.id) or 'ru'
    
    orders = db.get_pending_orders()
    
    if not orders:
        await callback.message.edit_text(
            text=get_text(user_lang, 'no_active_orders'),
            reply_markup=get_admin_keyboard(user_lang),
            parse_mode="HTML"
        )
        await callback.answer()
        return
    
    # Формируем список заказов с кнопками
    orders_text = get_text(user_lang, 'active_orders_title')
    
    buttons = []
    for order in orders:
        order_id, user_id, first_name, username, service_name, description, status, created_at = order
        status_emoji = "🟡" if status == "Pending" else "🔵"
        button_text = f"{status_emoji} #{order_id} | {first_name} | {service_name[:20]}"
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=f"order_view_{order_id}")])
    
    buttons.append([InlineKeyboardButton(text=get_text(user_lang, 'btn_back'), callback_data="back_to_admin")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await callback.message.edit_text(
        text=orders_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("order_view_"))
async def view_order_details(callback: types.CallbackQuery):
    """Показывает детали заказа"""
    user_id = callback.from_user.id
    
    # SECURITY: Проверка прав доступа (только admin)
    if not db.has_permission(user_id, 'admin'):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        logger.warning(f"⚠️ Попытка неавторизованного доступа к заказу: user_id={user_id}")
        return
    
    order_id = int(callback.data.split("_")[2])
    user_lang = db.get_user_language(callback.from_user.id) or 'ru'
    
    order = db.get_order_by_id(order_id)
    if not order:
        await callback.answer("❌ Заказ не найден", show_alert=True)
        return
    
    order_id, user_id, service_name, description, status = order
    
    # Получаем информацию о пользователе
    user_info = db.get_user_info(user_id)
    name = user_info['first_name'] if user_info else "Unknown"
    username = user_info['username'] if user_info else "no_username"
    
    status_map = {
        'Pending': get_text(user_lang, 'order_status_pending'),
        'In Progress': get_text(user_lang, 'order_status_in_progress'),
        'Done': get_text(user_lang, 'order_status_done'),
        'Cancelled': get_text(user_lang, 'order_status_cancelled')
    }
    
    order_text = get_text(
        user_lang,
        'order_details',
        order_id=order_id,
        name=name,
        username=username,
        user_id=user_id,
        service=service_name,
        description=description,
        status=status_map.get(status, status)
    )
    
    await callback.message.edit_text(
        text=order_text,
        reply_markup=get_order_management_keyboard(order_id, user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("order_status_"))
async def update_order_status_handler(callback: types.CallbackQuery):
    """Обновляет статус заказа и уведомляет пользователя"""
    user_id = callback.from_user.id
    
    # SECURITY: Проверка прав доступа (только admin)
    if not db.has_permission(user_id, 'admin'):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        logger.warning(f"⚠️ Попытка изменения статуса заказа: user_id={user_id}")
        return
    
    parts = callback.data.split("_")
    order_id = int(parts[2])
    new_status = " ".join(parts[3:])  # "In Progress", "Done", "Cancelled"
    
    # Обновляем статус
    db.update_order_status(order_id, new_status)
    
    # Получаем информацию о заказе
    order = db.get_order_by_id(order_id)
    if not order:
        await callback.answer("❌ Заказ не найден", show_alert=True)
        return
    
    _, user_id, service_name, _, _ = order
    
    # Получаем язык пользователя
    user_lang = db.get_user_language(user_id) or 'ru'
    
    status_map = {
        'Pending': get_text(user_lang, 'order_status_pending'),
        'In Progress': get_text(user_lang, 'order_status_in_progress'),
        'Done': get_text(user_lang, 'order_status_done'),
        'Cancelled': get_text(user_lang, 'order_status_cancelled')
    }
    
    # Отправляем уведомление пользователю
    notification_text = get_text(
        user_lang,
        'order_status_changed',
        order_id=order_id,
        service=service_name,
        status=status_map.get(new_status, new_status)
    )
    
    try:
        await callback.bot.send_message(
            chat_id=user_id,
            text=notification_text,
            parse_mode="HTML"
        )
        logger.info(f"✅ Уведомление о статусе заказа #{order_id} отправлено пользователю {user_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки уведомления: {e}")
    
    await callback.answer(f"✅ Статус изменен: {new_status}")
    
    # Возвращаемся к списку заказов
    await show_active_orders(callback)


@router.callback_query(F.data == "back_to_admin")
async def back_to_admin(callback: types.CallbackQuery):
    """Возврат в админ-панель"""
    user_id = callback.from_user.id
    
    # SECURITY: Проверка прав доступа (только admin)
    if not db.has_permission(user_id, 'admin'):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        return
    
    user_lang = db.get_user_language(callback.from_user.id) or 'ru'
    
    await callback.message.edit_text(
        text=get_text(user_lang, 'admin_panel'),
        reply_markup=get_admin_keyboard(user_lang),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: types.CallbackQuery, state: FSMContext):
    """Начинает рассылку"""
    user_id = callback.from_user.id
    
    # SECURITY: Проверка прав доступа (только admin)
    if not db.has_permission(user_id, 'admin'):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        logger.warning(f"⚠️ Попытка запуска рассылки: user_id={user_id}")
        return
    
    user_lang = db.get_user_language(callback.from_user.id) or 'ru'
    
    await state.set_state(BroadcastStates.waiting_for_message)
    
    await callback.message.edit_text(
        text=get_text(user_lang, 'broadcast_prompt'),
        parse_mode="HTML"
    )
    await callback.answer()


@router.message(BroadcastStates.waiting_for_message)
async def process_broadcast(message: types.Message, state: FSMContext):
    """Обрабатывает рассылку"""
    if message.from_user.id != config.ADMIN_ID:
        await state.clear()
        return
    
    user_lang = db.get_user_language(message.from_user.id) or 'ru'
    
    users = db.get_all_users()
    
    success = 0
    failed = 0
    
    status_message = await message.answer(
        f"📢 <b>Начинаю рассылку...</b>\n\n👥 Всего пользователей: {len(users)}",
        parse_mode="HTML"
    )
    
    for user_id, lang in users:
        try:
            if message.text:
                await message.bot.send_message(chat_id=user_id, text=message.text, parse_mode="HTML")
            elif message.photo:
                await message.bot.send_photo(
                    chat_id=user_id,
                    photo=message.photo[-1].file_id,
                    caption=message.caption,
                    parse_mode="HTML"
                )
            
            success += 1
            await asyncio.sleep(0.05)
            
        except Exception as e:
            failed += 1
            logger.warning(f"⚠️ Не удалось отправить сообщение пользователю {user_id}: {e}")
    
    await status_message.edit_text(
        text=get_text(user_lang, 'broadcast_success', success=success, failed=failed),
        parse_mode="HTML"
    )
    
    logger.info(f"📢 Рассылка завершена: успешно={success}, ошибок={failed}")
    
    await state.clear()


# ============= НОВАЯ ФУНКЦИЯ: НАПИСАТЬ ПО ID =============

@router.callback_query(F.data == "admin_reply_id")
async def admin_reply_by_id_start(callback: types.CallbackQuery, state: FSMContext):
    """Начинает процесс отправки сообщения по ID"""
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    await callback.message.answer(
        text="✉️ <b>Отправка сообщения по ID</b>\n\nВведите ID пользователя:",
        parse_mode="HTML"
    )
    
    await state.set_state(AdminReplyStates.waiting_for_user_id)
    await callback.answer()


@router.message(AdminReplyStates.waiting_for_user_id)
async def admin_reply_receive_id(message: types.Message, state: FSMContext):
    """Получает ID пользователя"""
    if message.from_user.id != config.ADMIN_ID:
        await state.clear()
        return
    
    # Проверяем что введены только цифры
    if not message.text.isdigit():
        await message.answer(
            text="❌ <b>Ошибка!</b>\n\nID должен состоять только из цифр.\nПопробуйте снова:",
            parse_mode="HTML"
        )
        return
    
    user_id = int(message.text)
    
    # Проверяем существует ли пользователь
    if not db.user_exists(user_id):
        await message.answer(
            text=f"❌ <b>Ошибка!</b>\n\nПользователь с ID <code>{user_id}</code> не найден в базе.\nВведите другой ID:",
            parse_mode="HTML"
        )
        return
    
    # Сохраняем ID в состояние
    await state.update_data(target_user_id=user_id)
    
    await message.answer(
        text=f"✅ ID получен: <code>{user_id}</code>\n\nТеперь введите текст сообщения:",
        parse_mode="HTML"
    )
    
    await state.set_state(AdminReplyStates.waiting_for_message)


@router.message(AdminReplyStates.waiting_for_message)
async def admin_reply_send_message(message: types.Message, state: FSMContext):
    """Отправляет сообщение пользователю"""
    if message.from_user.id != config.ADMIN_ID:
        await state.clear()
        return
    
    # Получаем ID из состояния
    data = await state.get_data()
    target_user_id = data.get('target_user_id')
    
    if not target_user_id:
        await message.answer("❌ Ошибка: ID не найден. Начните заново с /admin")
        await state.clear()
        return
    
    # Пытаемся отправить сообщение
    try:
        await message.bot.send_message(
            chat_id=target_user_id,
            text=message.text,
            parse_mode="HTML"
        )
        
        await message.answer(
            text=f"✅ <b>Сообщение доставлено!</b>\n\nПолучатель: <code>{target_user_id}</code>",
            parse_mode="HTML"
        )
        
        logger.info(f"✉️ Админ отправил сообщение пользователю {target_user_id}")
        
    except Exception as e:
        error_text = str(e)
        
        if "bot was blocked by the user" in error_text or "user is deactivated" in error_text:
            await message.answer(
                text=f"❌ <b>Ошибка: Бот заблокирован юзером</b>\n\nID: <code>{target_user_id}</code>",
                parse_mode="HTML"
            )
        else:
            await message.answer(
                text=f"❌ <b>Ошибка отправки:</b>\n\n<code>{error_text}</code>",
                parse_mode="HTML"
            )
        
        logger.error(f"❌ Ошибка отправки сообщения пользователю {target_user_id}: {e}")
    
    await state.clear()
