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

# Список всех роутеров для регистрации в главном файле
routers = [
    start_router,
    subscription_router,
    admin_router,
    services_router,
    profile_router,
    about_router,
    help_router,
    order_router
]

__all__ = ['routers']
