"""
Конфигурация бота Merix CodeX
Загружает переменные окружения из .env файла
"""
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота (получите у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID администратора для получения заказов
ADMIN_ID = os.getenv("ADMIN_ID")

# Проверка наличия обязательных переменных
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env файле!")

if not ADMIN_ID:
    raise ValueError("❌ ADMIN_ID не найден в .env файле!")

# Преобразуем ADMIN_ID в число
try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    raise ValueError("❌ ADMIN_ID должен быть числом!")

# ID канала для обязательной подписки
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHANNEL_URL = os.getenv("CHANNEL_URL")

if not CHANNEL_ID:
    raise ValueError("❌ CHANNEL_ID не найден в .env файле!")
if not CHANNEL_URL:
    raise ValueError("❌ CHANNEL_URL не найден в .env файле!")

# Прокси для обхода блокировок (опционально)
PROXY_URL = os.getenv("PROXY_URL", None)

# ID приватного канала для платных подписок (Merix Academy)
PRIVATE_CHANNEL_ID = -1003543534808

# Реквизиты для оплаты картой
PAYMENT_CARD_ALIF = "+992888788181"
PAYMENT_CARD_MASTERCARD = "5413525250170749"

# YooMoney настройки для платежей
YOOMONEY_TOKEN = "4100119383236022.B55A94F9434ACFAC33934F62C6E3FCC9A21203DEE377157D996B5422A0A9763F4808C7468B8BB4CD3B4B9C787FA55E333CAC7B7047F29004CCEDBC29F0AE54B277E66F5125706416CB6BEAB33F538F6C858557E6E2251AD08134ABCF38D9B14D8BB90DFCC85B934CAC790209816E737172314DC175C3573A89280F4D8B513E59"
YOOMONEY_WALLET = "+992947764004"  # Номер кошелька в профиле YooMoney
