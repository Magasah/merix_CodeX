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


class AdminReplyStates(StatesGroup):
    """Состояния для отправки сообщения пользователю по ID"""
    
    # Состояние: ожидание ID пользователя
    waiting_for_user_id = State()
    
    # Состояние: ожидание текста сообщения
    waiting_for_message = State()


class PaymentStates(StatesGroup):
    """Состояния для процесса пополнения баланса YooMoney"""
    
    # Состояние: ожидание суммы пополнения
    waiting_for_amount = State()


class InvoiceStates(StatesGroup):
    """Состояния для процесса выставления счёта администратором/менеджером"""
    
    # Состояние: ожидание ID пользователя
    waiting_for_user_id = State()
    
    # Состояние: ожидание суммы
    waiting_for_amount = State()
    
    # Состояние: ожидание описания услуги
    waiting_for_description = State()

