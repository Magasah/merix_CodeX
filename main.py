"""
Главный файл Telegram бота Merix CodeX Global - UPGRADED VERSION v2.0

Мультиязычный бот для IT-агентства с поддержкой:
- Русский, English, Тоҷикӣ, O'zbekcha
- База данных SQLite с реферальной системой
- Web App интеграция (https://merix-codex.netlify.app)
- Система отзывов с модерацией
- Расширенная админ-панель
- Новые пакеты услуг (Fast Start, AI Automation, Tech Support)

Технологии: aiogram 3.x, SQLite, FSM, i18n, WebApp
Автор: Senior Python Developer
Дата: 30 декабря 2025
"""
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import BotCommand

import config
import database as db
from handlers import routers
from middleware import ChannelSubscriptionMiddleware

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot):
    """Устанавливает команды бота в меню"""
    commands = [
        BotCommand(command="start", description="🚀 Перезапуск / Выбор языка"),
        BotCommand(command="help", description="🆘 Помощь и поддержка"),
        BotCommand(command="admin", description="🔐 Админ-панель (только для админа)")
    ]
    await bot.set_my_commands(commands)


async def main():
    """
    Главная функция запуска бота
    Инициализирует БД, бота, диспетчер и запускает polling
    """
    # Инициализируем базу данных
    logger.info("📦 Инициализация базы данных...")
    db.init_db()
    
    # Создаем сессию с прокси (если указан)
    # ДЛЯ PYTHONANYWHERE: раскомментируйте строку ниже и укажите прокси
    session = None
    if config.PROXY_URL:
        logger.info(f"🌐 Использование прокси: {config.PROXY_URL.split('@')[-1] if '@' in config.PROXY_URL else config.PROXY_URL}")
        session = AiohttpSession(proxy=config.PROXY_URL)
    # Пример для PythonAnywhere:
    # session = AiohttpSession(proxy="http://proxy.server:3128")
    
    # Создаем экземпляр бота
    bot = Bot(token=config.BOT_TOKEN, session=session)
    
    # Создаем диспетчер с хранилищем состояний FSM в памяти
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрируем middleware для проверки подписки на канал
    dp.message.middleware(ChannelSubscriptionMiddleware())
    dp.callback_query.middleware(ChannelSubscriptionMiddleware())
    
    # Регистрируем все роутеры
    for router in routers:
        dp.include_router(router)
    
    # Устанавливаем команды бота
    await set_bot_commands(bot)
    
    # Получаем информацию о боте
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    
    logger.info("=" * 60)
    logger.info("🤖 Бот Merix CodeX Global v2.0 UPGRADED запущен!")
    logger.info(f"📛 Имя бота: @{bot_username}")
    logger.info(f"📊 Зарегистрировано роутеров: {len(routers)}")
    logger.info(f"👨‍💼 ID администратора: {config.ADMIN_ID}")
    logger.info(f"📢 Обязательный канал: {config.CHANNEL_ID}")
    logger.info(f"🌍 Поддерживаемые языки: Русский, English, Тоҷикӣ, O'zbekcha")
    logger.info(f"🌐 Web App: https://merix-codex.netlify.app")
    logger.info(f"⭐ Новые фичи: Referral System, Reviews, New Packages")
    logger.info("=" * 60)
    
    try:
        # Удаляем старые обновления и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logger.info("⏹ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("✅ Бот успешно завершил работу")


if __name__ == "__main__":
    """
    Точка входа в приложение
    Запускает асинхронную главную функцию
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⛔ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
