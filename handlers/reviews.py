"""
Обработчик системы отзывов с модерацией
"""
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from translations import get_text
from keyboards.inline import get_reviews_keyboard
from states.order import ReviewStates
import database as db
import config
import logging

logger = logging.getLogger(__name__)

# Создаем роутер для обработчиков отзывов
router = Router()


@router.message(F.text.in_([
    "⭐ Отзывы", 
    "⭐ Reviews", 
    "⭐ Сарзина", 
    "⭐ Sharhlar"
]))
async def show_reviews_menu(message: types.Message):
    """
    Показывает меню отзывов
    """
    user = message.from_user
    
    # Получаем язык пользователя
    user_lang = db.get_user_language(user.id)
    if not user_lang:
        user_lang = 'ru'
    
    await message.answer(
        text=get_text(user_lang, 'reviews_menu'),
        reply_markup=get_reviews_keyboard(user_lang),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "write_review")
async def start_write_review(callback: types.CallbackQuery, state: FSMContext):
    """
    Начинает процесс написания отзыва
    """
    user = callback.from_user
    
    # Получаем язык пользователя
    user_lang = db.get_user_language(user.id)
    if not user_lang:
        user_lang = 'ru'
    
    # Переводим в состояние ожидания отзыва
    await state.set_state(ReviewStates.waiting_for_review)
    
    await callback.message.edit_text(
        text=get_text(user_lang, 'review_prompt'),
        parse_mode="HTML"
    )
    
    await callback.answer()


@router.message(ReviewStates.waiting_for_review)
async def process_review(message: types.Message, state: FSMContext):
    """
    Обрабатывает отзыв пользователя и отправляет админу на модерацию
    """
    user = message.from_user
    
    # Получаем язык пользователя
    user_lang = db.get_user_language(user.id)
    if not user_lang:
        user_lang = 'ru'
    
    # Отправляем отзыв админу на модерацию
    admin_text = get_text(
        'ru',  # Админу всегда на русском
        'review_to_admin',
        name=user.first_name or "Пользователь",
        username=user.username or "нет username",
        user_id=user.id,
        review=message.text
    )
    
    try:
        await message.bot.send_message(
            chat_id=config.ADMIN_ID,
            text=admin_text,
            parse_mode="HTML"
        )
        
        # Подтверждаем пользователю
        await message.answer(
            text=get_text(user_lang, 'review_sent'),
            parse_mode="HTML"
        )
        
        logger.info(f"⭐ Новый отзыв от пользователя {user.id} отправлен админу")
        
    except Exception as e:
        logger.error(f"❌ Ошибка отправки отзыва админу: {e}")
        await message.answer(
            text="❌ Произошла ошибка. Попробуйте позже.",
            parse_mode="HTML"
        )
    
    # Очищаем состояние
    await state.clear()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    """
    Возврат в главное меню
    """
    user = callback.from_user
    
    # Получаем язык пользователя
    user_lang = db.get_user_language(user.id)
    if not user_lang:
        user_lang = 'ru'
    
    await callback.message.edit_text(
        text=get_text(user_lang, 'welcome', name=user.first_name),
        parse_mode="HTML"
    )
    
    await callback.answer()
