"""Обработчик проверки подписки на канал"""
from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translations import get_text
from keyboards.reply import get_main_keyboard
import database as db
import config

router = Router()

@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: types.CallbackQuery):
    """Проверка подписки по нажатию кнопки"""
    user = callback.from_user
    user_lang = db.get_user_language(user.id) or 'ru'
    
    try:
        # Проверяем статус пользователя в канале
        member = await callback.bot.get_chat_member(
            chat_id=config.CHANNEL_ID,
            user_id=user.id
        )
        
        if member.status in ['member', 'administrator', 'creator']:
            # Пользователь подписан!
            # Проверяем, есть ли пользователь в БД
            if not db.user_exists(user.id):
                # Новый пользователь - показываем выбор языка
                from handlers.start import get_language_keyboard
                await callback.message.edit_text(
                    text=get_text('ru', 'choose_language'),
                    reply_markup=get_language_keyboard(),
                    parse_mode="HTML"
                )
            else:
                # Существующий пользователь - показываем главное меню
                await callback.message.delete()
                await callback.message.answer(
                    text=get_text(user_lang, 'welcome', name=user.first_name),
                    reply_markup=get_main_keyboard(user_lang),
                    parse_mode="HTML"
                )
            await callback.answer("✅ " + get_text(user_lang, 'subscription_confirmed'), show_alert=False)
        else:
            # Все еще не подписан
            await callback.answer(
                get_text(user_lang, 'please_subscribe'),
                show_alert=True
            )
    except Exception as e:
        await callback.answer(
            f"❌ Ошибка проверки: {str(e)}",
            show_alert=True
        )
