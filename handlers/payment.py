"""
Обработчик платежей YooMoney
"""
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yoomoney import Quickpay, Client
from states.order import PaymentStates
import database as db
import config
import uuid
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "topup_balance")
async def topup_balance_start(callback: types.CallbackQuery, state: FSMContext):
    """Начинает процесс пополнения баланса"""
    if not config.YOOMONEY_ENABLED:
        await callback.answer("⚠️ Платежи временно недоступны", show_alert=True)
        await callback.message.answer(
            text="⚠️ <b>Платежная система временно не настроена.</b>\n\nОбратитесь к администратору.",
            parse_mode="HTML"
        )
        return

    await callback.message.answer(
        text=(
            "💳 <b>Пополнение баланса</b>\n\n"
            "Введите сумму пополнения в рублях (минимум 10 RUB):"
        ),
        parse_mode="HTML"
    )
    
    await state.set_state(PaymentStates.waiting_for_amount)
    await callback.answer()


@router.message(PaymentStates.waiting_for_amount)
async def process_payment_amount(message: types.Message, state: FSMContext):
    """Обрабатывает введённую сумму и создаёт платёж"""
    user_id = message.from_user.id
    
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
            text="❌ <b>Ошибка!</b>\n\nМинимальная сумма пополнения: 10 RUB\nПопробуйте снова:",
            parse_mode="HTML"
        )
        return
    
    # Генерируем уникальный label для отслеживания платежа
    payment_label = f"user_{user_id}_{uuid.uuid4().hex[:8]}"
    
    # Создаём ссылку на оплату через YooMoney
    try:
        quickpay = Quickpay(
            receiver=config.YOOMONEY_WALLET,
            quickpay_form="shop",
            targets=f"Пополнение баланса Merix CodeX",
            paymentType="SB",
            sum=amount,
            label=payment_label
        )
        
        payment_url = quickpay.redirected_url
        
        # Сохраняем данные в состояние
        await state.update_data(
            amount=amount,
            label=payment_label
        )
        
        # Создаём клавиатуру с кнопками
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url=payment_url)],
                [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"check_pay_{payment_label}_{amount}")],
                [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_payment")]
            ]
        )
        
        await message.answer(
            text=(
                f"💳 <b>Счёт на оплату создан</b>\n\n"
                f"💰 Сумма: <b>{amount} RUB</b>\n"
                f"🆔 ID платежа: <code>{payment_label}</code>\n\n"
                f"1️⃣ Нажмите кнопку <b>\"💳 Оплатить\"</b>\n"
                f"2️⃣ Выполните оплату\n"
                f"3️⃣ Вернитесь и нажмите <b>\"✅ Я оплатил\"</b>\n\n"
                f"⚠️ Платёж будет проверен автоматически."
            ),
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
        logger.info(f"💳 Создана ссылка на оплату для пользователя {user_id}: {amount} RUB")
        
    except Exception as e:
        await message.answer(
            text=f"❌ <b>Ошибка создания платежа:</b>\n\n<code>{str(e)}</code>",
            parse_mode="HTML"
        )
        logger.error(f"❌ Ошибка создания платежа YooMoney: {e}")
        await state.clear()


@router.callback_query(F.data.startswith("check_pay_"))
async def check_payment_status(callback: types.CallbackQuery, state: FSMContext):
    """Проверяет статус платежа через YooMoney API"""
    if not config.YOOMONEY_TOKEN:
        await callback.answer("⚠️ Проверка платежа недоступна", show_alert=True)
        return

    user_id = callback.from_user.id
    
    # Извлекаем label и amount из callback_data
    parts = callback.data.split("_")
    if len(parts) < 5:
        await callback.answer("❌ Ошибка: неверный формат данных", show_alert=True)
        return
    
    payment_label = "_".join(parts[2:-1])  # user_123_abc123
    amount = int(parts[-1])
    
    await callback.message.edit_text(
        text="🔄 <b>Проверяю платёж...</b>\n\nПожалуйста, подождите.",
        parse_mode="HTML"
    )
    
    try:
        # Подключаемся к YooMoney API
        client = Client(config.YOOMONEY_TOKEN)
        
        # Получаем историю операций с фильтром по label
        history = client.operation_history(label=payment_label)
        
        # Проверяем есть ли успешные платежи
        payment_found = False
        
        if history.operations:
            for operation in history.operations:
                if operation.label == payment_label and operation.status == "success":
                    payment_found = True
                    
                    # Начисляем баланс
                    db.update_user_balance(user_id, amount)
                    
                    # Получаем новый баланс
                    new_balance = db.get_user_balance(user_id)
                    
                    await callback.message.edit_text(
                        text=(
                            f"✅ <b>Платёж успешно подтверждён!</b>\n\n"
                            f"💰 Начислено: <b>{amount} RUB</b>\n"
                            f"💳 Ваш баланс: <b>{new_balance} RUB</b>\n\n"
                            f"Спасибо за пополнение!"
                        ),
                        parse_mode="HTML"
                    )
                    
                    logger.info(f"✅ Платёж подтверждён: user={user_id}, amount={amount} RUB, label={payment_label}")
                    
                    await state.clear()
                    break
        
        if not payment_found:
            # Создаём кнопку для повторной проверки
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔄 Проверить снова", callback_data=f"check_pay_{payment_label}_{amount}")],
                    [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_payment")]
                ]
            )
            
            await callback.message.edit_text(
                text=(
                    "⏳ <b>Платёж пока не найден</b>\n\n"
                    "Возможные причины:\n"
                    "• Платёж ещё обрабатывается (подождите 1-2 минуты)\n"
                    "• Вы ещё не завершили оплату\n\n"
                    "Проверьте статус платежа и нажмите <b>\"🔄 Проверить снова\"</b>"
                ),
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        
        await callback.answer()
        
    except Exception as e:
        await callback.message.edit_text(
            text=(
                f"❌ <b>Ошибка проверки платежа:</b>\n\n"
                f"<code>{str(e)}</code>\n\n"
                f"Попробуйте позже или свяжитесь с поддержкой."
            ),
            parse_mode="HTML"
        )
        logger.error(f"❌ Ошибка проверки платежа YooMoney: {e}")
        await callback.answer()


@router.callback_query(F.data == "cancel_payment")
async def cancel_payment(callback: types.CallbackQuery, state: FSMContext):
    """Отменяет процесс пополнения"""
    await callback.message.edit_text(
        text="❌ <b>Пополнение баланса отменено</b>",
        parse_mode="HTML"
    )
    
    await state.clear()
    await callback.answer()
