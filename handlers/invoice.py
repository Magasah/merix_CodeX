"""
Обработчик выставления счетов администратором/менеджером
"""
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yoomoney import Quickpay
from states.order import InvoiceStates
import database as db
import config
import uuid
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "create_invoice")
async def create_invoice_start(callback: types.CallbackQuery, state: FSMContext):
    """Начинает процесс создания счёта (только для admin/manager)"""
    if not config.YOOMONEY_ENABLED:
        await callback.answer("⚠️ YooMoney не настроен", show_alert=True)
        return

    user_id = callback.from_user.id
    
    # SECURITY: Проверка прав доступа
    if not db.has_permission(user_id, 'manager'):
        await callback.answer("⛔ Доступ запрещён", show_alert=True)
        logger.warning(f"⚠️ Попытка неавторизованного доступа к созданию счёта: user_id={user_id}")
        return
    
    await callback.message.answer(
        text=(
            "🧾 <b>Создание счёта для клиента</b>\n\n"
            "Введите ID пользователя:"
        ),
        parse_mode="HTML"
    )
    
    await state.set_state(InvoiceStates.waiting_for_user_id)
    await callback.answer()


@router.message(InvoiceStates.waiting_for_user_id)
async def invoice_receive_user_id(message: types.Message, state: FSMContext):
    """Получает ID пользователя для выставления счёта"""
    user_id = message.from_user.id
    
    # SECURITY: Повторная проверка прав
    if not db.has_permission(user_id, 'manager'):
        await message.answer("⛔ Доступ запрещён")
        await state.clear()
        return
    
    # Проверяем что введены только цифры
    if not message.text.isdigit():
        await message.answer(
            text="❌ <b>Ошибка!</b>\n\nID должен состоять только из цифр.\nПопробуйте снова:",
            parse_mode="HTML"
        )
        return
    
    target_user_id = int(message.text)
    
    # Проверяем существует ли пользователь
    if not db.user_exists(target_user_id):
        await message.answer(
            text=f"❌ <b>Ошибка!</b>\n\nПользователь с ID <code>{target_user_id}</code> не найден в базе.\nВведите другой ID:",
            parse_mode="HTML"
        )
        return
    
    # Сохраняем ID в состояние
    await state.update_data(target_user_id=target_user_id)
    
    await message.answer(
        text=f"✅ ID получен: <code>{target_user_id}</code>\n\nТеперь введите сумму счёта (в рублях, минимум 10):",
        parse_mode="HTML"
    )
    
    await state.set_state(InvoiceStates.waiting_for_amount)


@router.message(InvoiceStates.waiting_for_amount)
async def invoice_receive_amount(message: types.Message, state: FSMContext):
    """Получает сумму счёта"""
    user_id = message.from_user.id
    
    # SECURITY: Повторная проверка прав
    if not db.has_permission(user_id, 'manager'):
        await message.answer("⛔ Доступ запрещён")
        await state.clear()
        return
    
    # Проверяем что введено число
    if not message.text.isdigit():
        await message.answer(
            text="❌ <b>Ошибка!</b>\n\nВведите корректную сумму (только цифры):",
            parse_mode="HTML"
        )
        return
    
    amount = int(message.text)
    
    # Проверяем минимальную сумму
    if amount < 10:
        await message.answer(
            text="❌ <b>Ошибка!</b>\n\nМинимальная сумма: 10 RUB\nПопробуйте снова:",
            parse_mode="HTML"
        )
        return
    
    # Сохраняем сумму в состояние
    await state.update_data(amount=amount)
    
    await message.answer(
        text=f"✅ Сумма: <b>{amount} RUB</b>\n\nТеперь введите описание услуги (за что платим):",
        parse_mode="HTML"
    )
    
    await state.set_state(InvoiceStates.waiting_for_description)


@router.message(InvoiceStates.waiting_for_description)
async def invoice_receive_description(message: types.Message, state: FSMContext):
    """Получает описание и создаёт счёт"""
    user_id = message.from_user.id
    
    # SECURITY: Повторная проверка прав
    if not db.has_permission(user_id, 'manager'):
        await message.answer("⛔ Доступ запрещён")
        await state.clear()
        return
    
    description = message.text
    
    # Получаем данные из состояния
    data = await state.get_data()
    target_user_id = data.get('target_user_id')
    amount = data.get('amount')
    
    if not target_user_id or not amount:
        await message.answer("❌ Ошибка: данные не найдены. Начните заново.")
        await state.clear()
        return
    
    # Генерируем уникальный label
    payment_label = f"invoice_{target_user_id}_{uuid.uuid4().hex[:8]}"
    
    # Создаём ссылку на оплату через YooMoney
    try:
        quickpay = Quickpay(
            receiver=config.YOOMONEY_WALLET,
            quickpay_form="shop",
            targets=f"Оплата: {description}",
            paymentType="SB",
            sum=amount,
            label=payment_label
        )
        
        payment_url = quickpay.redirected_url
        
        # Создаём клавиатуру для клиента
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить сейчас", url=payment_url)],
                [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"check_pay_{payment_label}_{amount}")]
            ]
        )
        
        # Отправляем счёт клиенту
        try:
            await message.bot.send_message(
                chat_id=target_user_id,
                text=(
                    f"🧾 <b>Вам выставлен счёт!</b>\n\n"
                    f"📝 <b>Услуга:</b> {description}\n"
                    f"💰 <b>Сумма:</b> {amount} RUB\n"
                    f"🆔 <b>ID счёта:</b> <code>{payment_label}</code>\n\n"
                    f"Нажмите кнопку ниже для оплаты:"
                ),
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            
            # Уведомляем менеджера об успехе
            await message.answer(
                text=(
                    f"✅ <b>Счёт успешно выставлен!</b>\n\n"
                    f"👤 Клиент: <code>{target_user_id}</code>\n"
                    f"💰 Сумма: <b>{amount} RUB</b>\n"
                    f"📝 Описание: {description}\n"
                    f"🆔 Label: <code>{payment_label}</code>"
                ),
                parse_mode="HTML"
            )
            
            logger.info(f"🧾 Счёт выставлен: manager={user_id}, client={target_user_id}, amount={amount}, label={payment_label}")
            
        except Exception as e:
            await message.answer(
                text=f"❌ <b>Ошибка отправки счёта клиенту:</b>\n\n<code>{str(e)}</code>\n\nВозможно, бот заблокирован пользователем.",
                parse_mode="HTML"
            )
            logger.error(f"❌ Ошибка отправки счёта клиенту {target_user_id}: {e}")
        
    except Exception as e:
        await message.answer(
            text=f"❌ <b>Ошибка создания платежа:</b>\n\n<code>{str(e)}</code>",
            parse_mode="HTML"
        )
        logger.error(f"❌ Ошибка создания счёта YooMoney: {e}")
    
    await state.clear()
