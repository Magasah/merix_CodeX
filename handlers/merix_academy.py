"""
Обработчики платной подписки на Merix Academy (Приватный канал)
Поддержка оплаты через Telegram Stars (XTR) и Ручной оплаты картой
"""
from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, InputMediaPhoto
from keyboards.inline import (
    get_subscription_plans_keyboard,
    get_payment_approval_keyboard
)
from states.order import SubscriptionStates
import config
import logging

router = Router()
logger = logging.getLogger(__name__)

# Placeholder изображение для Merix Academy
ACADEMY_PHOTO_URL = "https://via.placeholder.com/800x400.png?text=Merix+Academy"

# Словарь с тарифами (payload: (дни, цена, название))
SUBSCRIPTION_PLANS = {
    "sub_7_days": (7, 100, "7 Дней"),
    "sub_14_days": (14, 130, "14 Дней"),
    "sub_30_days": (30, 300, "30 Дней")
}


@router.callback_query(F.data == "merix_academy")
async def show_merix_academy(callback: types.CallbackQuery):
    """Показывает информацию о Merix Academy и тарифы"""
    
    description = (
        "🔐 <b>MERIX ACADEMY (PRIVACY CLUB)</b>\n\n"
        "Доступ к закрытой базе знаний студии Merix CodeX:\n"
        "🚀 <b>+100 Скриптов:</b> Готовые боты, парсеры, юзерботы.\n"
        "🛡 <b>CyberSecurity:</b> Курсы по этичному хакингу и защите.\n"
        "💻 <b>Frontend & Backend:</b> Обучение с нуля до PRO.\n"
        "🎁 <b>Шаблоны:</b> Готовые решения для продаж.\n\n"
        "👇 <b>Выберите тариф доступа:</b>"
    )
    
    try:
        # Пытаемся отредактировать сообщение с фото
        media = InputMediaPhoto(
            media=ACADEMY_PHOTO_URL,
            caption=description,
            parse_mode="HTML"
        )
        await callback.message.edit_media(
            media=media,
            reply_markup=get_subscription_plans_keyboard()
        )
    except Exception as e:
        # Если редактирование не удалось (например, нет фото), отправляем новое сообщение
        logger.warning(f"Не удалось отредактировать сообщение: {e}")
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=ACADEMY_PHOTO_URL,
            caption=description,
            reply_markup=get_subscription_plans_keyboard(),
            parse_mode="HTML"
        )
    
    await callback.answer()


@router.callback_query(F.data.startswith("sub_"))
async def process_subscription_payment(callback: types.CallbackQuery):
    """Обрабатывает выбор тарифа и отправляет инвойс через Telegram Stars"""
    
    plan_key = callback.data
    
    if plan_key not in SUBSCRIPTION_PLANS:
        await callback.answer("❌ Неверный тариф!", show_alert=True)
        return
    
    days, price, plan_name = SUBSCRIPTION_PLANS[plan_key]
    
    # Формируем инвойс для оплаты через Telegram Stars
    prices = [LabeledPrice(label=f"Подписка на {plan_name}", amount=price)]
    
    try:
        await callback.message.answer_invoice(
            title=f"🎓 Merix Academy — {plan_name}",
            description=(
                f"Доступ к приватному каналу Merix Academy на {days} дней.\n\n"
                "🚀 +100 скриптов\n"
                "🛡 Курсы по CyberSecurity\n"
                "💻 Обучение Frontend & Backend\n"
                "🎁 Готовые шаблоны"
            ),
            payload=plan_key,
            provider_token="",  # Для Telegram Stars токен не требуется
            currency="XTR",  # Валюта Telegram Stars
            prices=prices
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка при отправке инвойса: {e}")
        await callback.answer("❌ Ошибка при создании счета. Попробуйте позже.", show_alert=True)


@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):
    """Подтверждает предварительную проверку оплаты"""
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment_handler(message: types.Message, bot: Bot):
    """Обрабатывает успешную оплату через Telegram Stars"""
    
    payment_info = message.successful_payment
    plan_key = payment_info.invoice_payload
    
    # Проверяем валидность payload
    if plan_key not in SUBSCRIPTION_PLANS:
        await message.answer("❌ Ошибка: неверный тариф в платеже!")
        return
    
    days, price, plan_name = SUBSCRIPTION_PLANS[plan_key]
    user_id = message.from_user.id
    
    # Генерируем одноразовую ссылку-приглашение
    try:
        invite_link = await bot.create_chat_invite_link(
            chat_id=config.PRIVATE_CHANNEL_ID,
            member_limit=1,  # Ссылка для одного человека
            name=f"Sub_{user_id}_{plan_name}"
        )
        
        success_message = (
            "✅ <b>Оплата прошла успешно!</b>\n\n"
            f"💎 Тариф: <b>{plan_name}</b>\n"
            f"💰 Сумма: <b>{price} Stars</b>\n\n"
            f"🔗 <b>Вот ваша ссылка на вход:</b>\n"
            f"{invite_link.invite_link}\n\n"
            f"⚠️ <i>Ссылка одноразовая и работает только для вас!</i>"
        )
        
        await message.answer(success_message, parse_mode="HTML")
        
        # Уведомляем админа
        admin_notification = (
            "💰 <b>Новая подписка на Merix Academy!</b>\n\n"
            f"👤 Пользователь: {message.from_user.full_name} (@{message.from_user.username or 'без username'})\n"
            f"🆔 User ID: <code>{user_id}</code>\n"
            f"💎 Тариф: {plan_name}\n"
            f"💰 Сумма: {price} Stars"
        )
        await bot.send_message(config.ADMIN_ID, admin_notification, parse_mode="HTML")
        
    except Exception as e:
        logger.error(f"Ошибка при создании инвайт-ссылки: {e}")
        await message.answer(
            "❌ Произошла ошибка при создании ссылки. "
            "Обратитесь в поддержку @noxsec"
        )


@router.callback_query(F.data == "pay_manual")
async def show_manual_payment(callback: types.CallbackQuery, state: FSMContext):
    """Показывает реквизиты для ручной оплаты картой"""
    
    payment_info = (
        "💳 <b>Реквизиты для оплаты:</b>\n\n"
        "🏦 <b>Alif Mobi / DC City:</b>\n"
        f"<code>{config.PAYMENT_CARD_ALIF}</code>\n"
        "<i>(Нажмите на номер, чтобы скопировать)</i>\n\n"
        "💳 <b>MasterCard:</b>\n"
        f"<code>{config.PAYMENT_CARD_MASTERCARD}</code>\n\n"
        "⚠️ <b>После оплаты отправьте скриншот чека в этот чат.</b>"
    )
    
    await callback.message.edit_text(payment_info, parse_mode="HTML")
    await state.set_state(SubscriptionStates.waiting_for_receipt)
    await callback.answer()


@router.message(SubscriptionStates.waiting_for_receipt, F.photo)
async def receive_payment_receipt(message: types.Message, state: FSMContext, bot: Bot):
    """Получает скриншот чека и отправляет админу на подтверждение"""
    
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    username = message.from_user.username or "без username"
    
    # Пересылаем фото админу
    admin_message = (
        "💳 <b>Новый запрос на подтверждение оплаты подписки!</b>\n\n"
        f"👤 Пользователь: {user_name} (@{username})\n"
        f"🆔 User ID: <code>{user_id}</code>\n\n"
        "📸 Скриншот чека прикреплен ниже:"
    )
    
    try:
        await bot.send_message(
            config.ADMIN_ID,
            admin_message,
            parse_mode="HTML"
        )
        
        await bot.send_photo(
            config.ADMIN_ID,
            photo=message.photo[-1].file_id,
            reply_markup=get_payment_approval_keyboard(user_id)
        )
        
        await message.answer(
            "✅ Ваш чек отправлен на проверку!\n"
            "⏳ Ожидайте подтверждения от администратора."
        )
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Ошибка при отправке чека админу: {e}")
        await message.answer("❌ Ошибка при отправке чека. Попробуйте позже.")


@router.message(SubscriptionStates.waiting_for_receipt)
async def invalid_receipt_format(message: types.Message):
    """Обрабатывает неверный формат (не фото)"""
    await message.answer(
        "⚠️ Пожалуйста, отправьте <b>фото</b> чека об оплате.",
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("approve_pay_"))
async def approve_manual_payment(callback: types.CallbackQuery, bot: Bot):
    """Админ подтверждает оплату и выдает доступ"""
    
    user_id = int(callback.data.split("_")[-1])
    
    try:
        # Генерируем инвайт-ссылку для пользователя
        invite_link = await bot.create_chat_invite_link(
            chat_id=config.PRIVATE_CHANNEL_ID,
            member_limit=1,
            name=f"Manual_Sub_{user_id}"
        )
        
        # Отправляем ссылку пользователю
        user_message = (
            "✅ <b>Оплата подтверждена!</b>\n\n"
            "🔗 <b>Вот ваша ссылка на вход в Merix Academy:</b>\n"
            f"{invite_link.invite_link}\n\n"
            "⚠️ <i>Ссылка одноразовая и работает только для вас!</i>"
        )
        await bot.send_message(user_id, user_message, parse_mode="HTML")
        
        # Уведомляем админа
        await callback.message.answer("✅ Оплата подтверждена! Ссылка отправлена пользователю.")
        await callback.answer("Оплата подтверждена!")
        
    except Exception as e:
        logger.error(f"Ошибка при подтверждении оплаты: {e}")
        await callback.answer(f"❌ Ошибка: {e}", show_alert=True)


@router.callback_query(F.data.startswith("reject_pay_"))
async def reject_manual_payment(callback: types.CallbackQuery, bot: Bot):
    """Админ отклоняет оплату"""
    
    user_id = int(callback.data.split("_")[-1])
    
    try:
        # Уведомляем пользователя
        user_message = (
            "❌ <b>Оплата не подтверждена</b>\n\n"
            "Ваш чек был проверен, но оплата не прошла.\n"
            "Пожалуйста, свяжитесь с поддержкой: @noxsec"
        )
        await bot.send_message(user_id, user_message, parse_mode="HTML")
        
        # Уведомляем админа
        await callback.message.answer("❌ Оплата отклонена. Пользователь уведомлен.")
        await callback.answer("Оплата отклонена!")
        
    except Exception as e:
        logger.error(f"Ошибка при отклонении оплаты: {e}")
        await callback.answer(f"❌ Ошибка: {e}", show_alert=True)
