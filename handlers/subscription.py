"""Обработчик проверки подписки на канал"""
from aiogram import Router, F, types
import logging
from translations import get_text
from keyboards.reply import get_main_keyboard
import database as db
import config

router = Router()
logger = logging.getLogger(__name__)
MEMBER_LIST_WARNING_LOGGED = False


async def _proceed_after_subscription_confirmed(callback: types.CallbackQuery, user_lang: str):
    """Продолжает сценарий после подтверждения подписки или fallback-проверки"""
    user = callback.from_user

    if not db.user_exists(user.id):
        from handlers.start import get_language_keyboard
        await callback.message.edit_text(
            text=get_text('ru', 'choose_language'),
            reply_markup=get_language_keyboard(),
            parse_mode="HTML"
        )
    else:
        await callback.message.delete()
        await callback.message.answer(
            text=get_text(user_lang, 'welcome', name=user.first_name),
            reply_markup=get_main_keyboard(user_lang),
            parse_mode="HTML"
        )

@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: types.CallbackQuery):
    """Проверка подписки по нажатию кнопки"""
    user = callback.from_user
    user_lang = db.get_user_language(user.id) or 'ru'
    
    global MEMBER_LIST_WARNING_LOGGED

    try:
        # Проверяем статус пользователя в канале
        member = await callback.bot.get_chat_member(
            chat_id=config.CHANNEL_ID,
            user_id=user.id
        )
        
        if member.status in ['member', 'administrator', 'creator']:
            await _proceed_after_subscription_confirmed(callback, user_lang)
            await callback.answer("✅ " + get_text(user_lang, 'subscription_confirmed'), show_alert=False)
        else:
            # Все еще не подписан
            await callback.answer(
                get_text(user_lang, 'please_subscribe'),
                show_alert=True
            )
    except Exception as e:
        error_text = str(e).lower()
        if "member list is inaccessible" in error_text:
            if not MEMBER_LIST_WARNING_LOGGED:
                logger.warning("⚠️ Проверка подписки недоступна: member list is inaccessible")
                MEMBER_LIST_WARNING_LOGGED = True
            await _proceed_after_subscription_confirmed(callback, user_lang)
            await callback.answer("✅ " + get_text(user_lang, 'subscription_confirmed'), show_alert=False)
            return

        logger.warning(f"⚠️ Ошибка проверки подписки: {e}")
        await callback.answer(
            "❌ Проверка подписки временно недоступна. Попробуйте позже.",
            show_alert=True
        )
