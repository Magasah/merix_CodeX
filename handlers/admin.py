"""
Обработчик админ-панели с расширенной статистикой и рассылкой
"""
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from translations import get_text
from keyboards.inline import get_admin_keyboard
from states.order import BroadcastStates
import database as db
import config
import asyncio
import logging

logger = logging.getLogger(__name__)

# Создаем роутер для обработчиков админ-панели
router = Router()


@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    """
    Показывает админ-панель (только для администратора)
    """
    user = message.from_user
    
    # Проверка прав администратора
    if user.id != config.ADMIN_ID:
        await message.answer(
            text=get_text('ru', 'not_admin'),
            parse_mode="HTML"
        )
        return
    
    # Получаем язык пользователя
    user_lang = db.get_user_language(user.id)
    if not user_lang:
        user_lang = 'ru'
    
    await message.answer(
        text=get_text(user_lang, 'admin_panel'),
        reply_markup=get_admin_keyboard(user_lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin_stats")
async def show_statistics(callback: types.CallbackQuery):
    """
    Показывает расширенную статистику бота
    """
    # Проверка прав администратора
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    # Получаем язык пользователя
    user_lang = db.get_user_language(callback.from_user.id)
    if not user_lang:
        user_lang = 'ru'
    
    # Получаем статистику
    total_users = db.get_users_count()
    today_users = db.get_users_count_today()
    
    stats_text = get_text(
        user_lang,
        'statistics_text',
        total=total_users,
        today=today_users
    )
    
    await callback.message.edit_text(
        text=stats_text,
        reply_markup=get_admin_keyboard(user_lang),
        parse_mode="HTML"
    )
    
    await callback.answer()


@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: types.CallbackQuery, state: FSMContext):
    """
    Начинает процесс рассылки
    """
    # Проверка прав администратора
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    
    # Получаем язык пользователя
    user_lang = db.get_user_language(callback.from_user.id)
    if not user_lang:
        user_lang = 'ru'
    
    # Переводим в состояние ожидания сообщения
    await state.set_state(BroadcastStates.waiting_for_message)
    
    await callback.message.edit_text(
        text=get_text(user_lang, 'broadcast_prompt'),
        parse_mode="HTML"
    )
    
    await callback.answer()


@router.message(BroadcastStates.waiting_for_message)
async def process_broadcast(message: types.Message, state: FSMContext):
    """
    Обрабатывает рассылку сообщения всем пользователям
    С защитой от flood limits (asyncio.sleep(0.05))
    """
    # Проверка прав администратора
    if message.from_user.id != config.ADMIN_ID:
        await message.answer(text=get_text('ru', 'not_admin'), parse_mode="HTML")
        await state.clear()
        return
    
    # Получаем язык админа
    user_lang = db.get_user_language(message.from_user.id)
    if not user_lang:
        user_lang = 'ru'
    
    # Сохраняем сообщение для рассылки
    broadcast_text = message.text if message.text else message.caption
    
    # Получаем всех пользователей
    users = db.get_all_users()
    
    success = 0
    failed = 0
    
    # Отправляем сообщение о начале рассылки
    status_message = await message.answer(
        f"📢 <b>Начинаю рассылку...</b>\n\n"
        f"👥 Всего пользователей: {len(users)}",
        parse_mode="HTML"
    )
    
    # Рассылка с задержкой
    for user_id, lang in users:
        try:
            # Пересылаем сообщение пользователю
            if message.text:
                await message.bot.send_message(
                    chat_id=user_id,
                    text=broadcast_text,
                    parse_mode="HTML"
                )
            elif message.photo:
                await message.bot.send_photo(
                    chat_id=user_id,
                    photo=message.photo[-1].file_id,
                    caption=broadcast_text,
                    parse_mode="HTML"
                )
            
            success += 1
            
            # Задержка для избежания flood limits
            await asyncio.sleep(0.05)
            
        except Exception as e:
            failed += 1
            logger.warning(f"⚠️ Не удалось отправить сообщение пользователю {user_id}: {e}")
    
    # Обновляем статус
    await status_message.edit_text(
        text=get_text(
            user_lang,
            'broadcast_success',
            success=success,
            failed=failed
        ),
        parse_mode="HTML"
    )
    
    logger.info(f"📢 Рассылка завершена: успешно={success}, ошибок={failed}")
    
    # Очищаем состояние
    await state.clear()
