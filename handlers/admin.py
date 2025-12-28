"""Админ-панель с статистикой и рассылкой"""
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.inline import get_admin_keyboard
from translations import get_text
import database as db
import config
import asyncio

router = Router()

class BroadcastStates(StatesGroup):
    waiting_for_message = State()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != config.ADMIN_ID:
        user_lang = db.get_user_language(message.from_user.id) or 'ru'
        await message.answer(get_text(user_lang, 'not_admin'))
        return
    await message.answer(text=get_text('ru', 'admin_panel'), 
                        reply_markup=get_admin_keyboard('ru'), parse_mode="HTML")

@router.callback_query(F.data == "admin_stats")
async def show_statistics(callback: types.CallbackQuery):
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    count = db.get_user_count()
    await callback.message.edit_text(text=get_text('ru', 'statistics_text', count=count),
                                    reply_markup=get_admin_keyboard('ru'), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id != config.ADMIN_ID:
        await callback.answer("❌ Доступ запрещен", show_alert=True)
        return
    await state.set_state(BroadcastStates.waiting_for_message)
    await callback.message.answer(text=get_text('ru', 'broadcast_prompt'), parse_mode="HTML")
    await callback.answer()

@router.message(BroadcastStates.waiting_for_message)
async def process_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id != config.ADMIN_ID:
        return
    users = db.get_all_users()
    success = 0
    failed = 0
    status_message = await message.answer("📢 Начинаю рассылку...")
    for user_id, user_lang in users:
        try:
            await message.bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id, message_id=message.message_id)
            success += 1
            if success % 10 == 0:
                await status_message.edit_text(f"📤 Отправлено: {success}/{len(users)}")
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1
    await status_message.edit_text(text=get_text('ru', 'broadcast_success', success=success, failed=failed), parse_mode="HTML")
    await state.clear()
