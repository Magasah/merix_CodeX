"""
Модуль обработчиков команд и сообщений бота
"""
from .start import router as start_router
from .subscription import router as subscription_router
from .services import router as services_router
from .profile import router as profile_router
from .about import router as about_router
from .help import router as help_router
from .order import router as order_router
from .admin import router as admin_router
from .merix_academy import router as academy_router
from .payment import router as payment_router
from .invoice import router as invoice_router
from .manager import router as manager_router

# Список всех роутеров для регистрации в главном файле
routers = [
    start_router,
    subscription_router,
    admin_router,
    manager_router,  # Роутер для менеджерской панели и управления ролями
    payment_router,  # Роутер для YooMoney платежей
    invoice_router,  # Роутер для выставления счетов
    academy_router,  # Роутер для Merix Academy (должен быть перед services)
    services_router,
    profile_router,
    about_router,
    help_router,
    order_router
]

__all__ = ['routers']
