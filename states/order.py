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


class BroadcastStates(StatesGroup):
    """Состояния для процесса рассылки"""
    
    # Состояние: ожидание сообщения для рассылки
    waiting_for_message = State()


class ReviewStates(StatesGroup):
    """Состояния для процесса написания отзыва"""
    
    # Состояние: ожидание текста отзыва
    waiting_for_review = State()


class SubscriptionStates(StatesGroup):
    """Состояния для процесса оплаты подписки"""
    
    # Состояние: ожидание скриншота оплаты по карте
    waiting_for_receipt = State()

