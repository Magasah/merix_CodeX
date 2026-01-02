"""Обработчики раздела "Услуги" с мультиязычной поддержкой"""
from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline import get_services_keyboard, get_service_detail_keyboard
from translations import get_text
import database as db

router = Router()

@router.message(F.text.in_(["📂 Услуги", "📂 Services", "📂 Xizmatlar", "📂 Хизматрасонӣ"]))
async def show_services(message: types.Message):
    user_lang = db.get_user_language(message.from_user.id) or 'ru'
    db.update_last_interaction(message.from_user.id)
    await message.answer(text=get_text(user_lang, 'services_title'),
                        reply_markup=get_services_keyboard(user_lang, page=1), parse_mode="HTML")

@router.callback_query(F.data == "back_to_services")
async def back_to_services(callback: types.CallbackQuery):
    user_lang = db.get_user_language(callback.from_user.id) or 'ru'
    await callback.message.edit_text(text=get_text(user_lang, 'services_title'),
                                     reply_markup=get_services_keyboard(user_lang, page=1), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("services_page_"))
async def services_pagination(callback: types.CallbackQuery):
    """Обрабатывает переключение страниц меню услуг"""
    user_lang = db.get_user_language(callback.from_user.id) or 'ru'
    
    # Извлекаем номер страницы
    if callback.data == "services_page_info":
        await callback.answer()
        return
    
    page = int(callback.data.split("_")[-1])
    
    await callback.message.edit_text(
        text=get_text(user_lang, 'services_title'),
        reply_markup=get_services_keyboard(user_lang, page=page),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("service_"))
async def show_service_detail(callback: types.CallbackQuery):
    user_lang = db.get_user_language(callback.from_user.id) or 'ru'
    service_type = callback.data.split("_")[1]
    
    # Специальная обработка для service_scripts
    if service_type == "scripts":
        scripts_text = (
            "💻 <b>Разработка Скриптов и Софта</b>\n\n"
            "Мы пишем код под любые задачи:\n\n"
            "🎮 <b>GameDev:</b> Читы, боты для фарма, макросы (Roblox, Minecraft, Mobile).\n"
            "🕵️‍♂️ <b>Pentest & OSINT:</b> Парсеры, чеккеры, софт для тестов безопасности.\n"
            "🤖 <b>Automation:</b> Автоматизация рутины.\n\n"
            "💰 <b>Цена:</b> от 150 TJS (зависит от сложности).\n\n"
            "Для заказа нажмите кнопку ниже."
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="👨‍💻 Обсудить заказ", url="https://t.me/noxsec")],
                [InlineKeyboardButton(text=get_text(user_lang, 'btn_back'), callback_data="back_to_services")]
            ]
        )
        
        await callback.message.edit_text(
            text=scripts_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text(
            text=get_text(user_lang, f'service_{service_type}'),
            reply_markup=get_service_detail_keyboard(service_type, user_lang),
            parse_mode="HTML"
        )
    
    await callback.answer()
