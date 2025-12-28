"""
Главный файл Telegram бота Merix CodeX Global

Мультиязычный бот для IT-агентства с поддержкой:
- Русский, English, Тоҷикӣ, O'zbekcha
- База данных SQLite
- Админ-панель со статистикой и рассылкой
- Система заказов с FSM

Технологии: aiogram 3.x, SQLite, FSM, i18n
"""
import asyncio
import logging
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
        BotCommand(command="start", description="Перезапуск / Выбор языка"),
        BotCommand(command="help", description="Помощь и поддержка"),
        BotCommand(command="admin", description="Админ-панель (только для админа)")
    ]
    await bot.set_my_commands(commands)

# Импортируем все роутеры
from handlers import routers


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """
    Главная функция запуска бота
    Инициализирует БД, бота, диспетчер и запускает polling
    """
    # Инициализируем базу данных
    logger.info("📦 Инициализация базы данных...")
    db.init_db()
    
    # Создаем сессию с прокси (если указан)
    session = None
    if config.PROXY_URL:
        logger.info(f"🌐 Использование прокси: {config.PROXY_URL.split('@')[-1] if '@' in config.PROXY_URL else config.PROXY_URL}")
        session = AiohttpSession(proxy=config.PROXY_URL)
    
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
    
    logger.info("🤖 Бот Merix CodeX Global запущен!")
    logger.info(f"📊 Зарегистрировано роутеров: {len(routers)}")
    logger.info(f"👨‍💼 ID администратора: {config.ADMIN_ID}")
    logger.info(f"📢 Обязательный канал: {config.CHANNEL_ID}")
    logger.info(f"🌍 Поддерживаемые языки: Русский, English, Тоҷикӣ, O'zbekcha")
    
    try:
        # Удаляем старые обновления и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


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
