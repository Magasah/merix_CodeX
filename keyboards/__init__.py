"""
Модуль клавиатур для бота
"""
from .reply import get_main_keyboard
from .inline import (
    get_services_keyboard,
    get_service_detail_keyboard,
    get_order_confirmation_keyboard
)

__all__ = [
    'get_main_keyboard',
    'get_services_keyboard',
    'get_service_detail_keyboard',
    'get_order_confirmation_keyboard'
]
