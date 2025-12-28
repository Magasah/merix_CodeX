"""
Состояния FSM для процесса оформления заказа
"""
from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    """Состояния для процесса заказа услуги"""
    
    # Состояние: ожидание описания задачи от пользователя
    waiting_for_description = State()
    
    # Состояние: ожидание подтверждения заказа
    waiting_for_confirmation = State()
