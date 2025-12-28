"""Обработчики системы заказов с FSM и мультиязычной поддержкой"""
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from states.order import OrderStates
from keyboards.inline import get_order_confirmation_keyboard
from translations import get_text, LANGUAGE_NAMES
import database as db
import config

router = Router()

@router.callback_query(F.data.startswith("order_"))
async def start_order(callback: types.CallbackQuery, state: FSMContext):
    user_lang = db.get_user_language(callback.from_user.id) or 'ru'
    service_type = callback.data.split("_")[1]
    service_name = get_text(user_lang, f'btn_{service_type}')
    await state.update_data(service_type=service_type, service_name=service_name, user_lang=user_lang)
    await state.set_state(OrderStates.waiting_for_description)
    await callback.message.answer(text=get_text(user_lang, 'order_description', service=service_name), parse_mode="HTML")
    await callback.answer()

@router.message(OrderStates.waiting_for_description)
async def process_order_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_lang = data.get('user_lang', 'ru')
    await state.update_data(description=message.text)
    await state.set_state(OrderStates.waiting_for_confirmation)
    await message.answer(text=get_text(user_lang, 'order_confirmation', 
                                      service=data['service_name'], description=message.text),
                        reply_markup=get_order_confirmation_keyboard(user_lang), parse_mode="HTML")

@router.callback_query(F.data == "confirm_order", OrderStates.waiting_for_confirmation)
async def confirm_order(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = callback.from_user
    user_lang = data.get('user_lang', 'ru')
    username = f"@{user.username}" if user.username else "Не указан"
    admin_message = get_text('ru', 'admin_new_order', service=data['service_name'], 
                            name=user.full_name, username=username, user_id=user.id,
                            language=LANGUAGE_NAMES.get(user_lang, 'Русский'), description=data['description'])
    try:
        await callback.bot.send_message(chat_id=config.ADMIN_ID, text=admin_message, parse_mode="HTML")
        await callback.message.edit_text(text=get_text(user_lang, 'order_sent'), parse_mode="HTML")
    except Exception as e:
        await callback.message.edit_text(text=get_text(user_lang, 'order_error'), parse_mode="HTML")
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "cancel_order", OrderStates.waiting_for_confirmation)
async def cancel_order(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_lang = data.get('user_lang', 'ru')
    await state.clear()
    await callback.message.edit_text(text=get_text(user_lang, 'order_cancelled'), parse_mode="HTML")
    await callback.answer()
