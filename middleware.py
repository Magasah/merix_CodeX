"""
Middleware для проверки обязательной подписки на канал
"""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
import config
from translations import get_text
import database as db


class ChannelSubscriptionMiddleware(BaseMiddleware):
    """
    Middleware для проверки подписки пользователя на канал
    Блокирует доступ к боту если пользователь не подписан
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Определяем тип события и получаем user
        if isinstance(event, Message):
            user = event.from_user
            chat_id = event.chat.id
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            chat_id = event.message.chat.id if event.message else user.id
        else:
            # Для других типов событий просто пропускаем
            return await handler(event, data)
        
        # Пропускаем проверку для команды проверки подписки
        if isinstance(event, CallbackQuery) and event.data == "check_subscription":
            return await handler(event, data)
        
        # Получаем бота из data
        bot = data.get("bot")
        if not bot:
            return await handler(event, data)
        
        try:
            # Проверяем статус пользователя в канале
            member = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user.id)
            
            # Разрешенные статусы: member, administrator, creator
            if member.status not in ['member', 'administrator', 'creator']:
                # Пользователь не подписан
                await self.send_subscription_required(event, bot, user.id)
                return  # Блокируем дальнейшее выполнение
            
        except Exception as e:
            # Если произошла ошибка (например, бот не админ канала), логируем и пропускаем
            print(f"⚠️ Ошибка проверки подписки: {e}")
            # В production лучше блокировать доступ, но для разработки пропускаем
            pass
        
        # Пользователь подписан - продолжаем обработку
        return await handler(event, data)
    
    async def send_subscription_required(self, event: TelegramObject, bot, user_id: int):
        """Отправляет сообщение о необходимости подписки"""
        # Получаем язык пользователя или используем русский по умолчанию
        user_lang = db.get_user_language(user_id) or 'ru'
        
        # Создаем клавиатуру с кнопками подписки и проверки
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=get_text(user_lang, 'btn_subscribe'),
                    url=config.CHANNEL_URL
                )],
                [InlineKeyboardButton(
                    text=get_text(user_lang, 'btn_check_subscription'),
                    callback_data="check_subscription"
                )]
            ]
        )
        
        # Отправляем сообщение
        message_text = get_text(user_lang, 'subscription_required')
        
        if isinstance(event, Message):
            await event.answer(
                text=message_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        elif isinstance(event, CallbackQuery):
            if event.message:
                try:
                    await event.message.edit_text(
                        text=message_text,
                        reply_markup=keyboard,
                        parse_mode="HTML"
                    )
                except:
                    await bot.send_message(
                        chat_id=user_id,
                        text=message_text,
                        reply_markup=keyboard,
                        parse_mode="HTML"
                    )
            await event.answer(get_text(user_lang, 'please_subscribe'), show_alert=True)
