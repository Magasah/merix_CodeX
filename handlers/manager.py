"""
Панель управления для менеджеров и команды управления ролями
"""
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.order import AdminReplyStates
import database as db
import config
import logging

logger = logging.getLogger(__name__)

router = Router()


def get_manager_keyboard() -> InlineKeyboardMarkup:
    """Создаёт клавиатуру панели менеджера"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✉️ Ответить по ID", callback_data="admin_reply_id")],
            [InlineKeyboardButton(text="🧾 Выставить счёт", callback_data="create_invoice")]
        ]
    )
    return keyboard


@router.message(Command("staff"))
async def staff_panel(message: types.Message):
    """Панель для менеджеров и админов"""
    user_id = message.from_user.id
    
    # SECURITY: Проверка прав доступа
    if not db.has_permission(user_id, 'manager'):
        await message.answer(
            text="⛔ <b>Доступ запрещён</b>\n\nЭта команда доступна только персоналу.",
            parse_mode="HTML"
        )
        logger.warning(f"⚠️ Попытка неавторизованного доступа к /staff: user_id={user_id}")
        return
    
    user_role = db.get_user_role(user_id)
    role_emoji = "👨‍💼" if user_role == "manager" else "👑"
    
    await message.answer(
        text=(
            f"{role_emoji} <b>Панель персонала</b>\n\n"
            f"👤 Ваша роль: <b>{user_role.upper()}</b>\n\n"
            f"Выберите действие:"
        ),
        reply_markup=get_manager_keyboard(),
        parse_mode="HTML"
    )


# ============= КОМАНДЫ УПРАВЛЕНИЯ РОЛЯМИ (ТОЛЬКО ADMIN) =============

@router.message(Command("set_manager"))
async def set_manager_command(message: types.Message):
    """Назначает пользователя менеджером (только admin)"""
    user_id = message.from_user.id
    
    # SECURITY: Только admin может назначать менеджеров
    if user_id != config.ADMIN_ID:
        await message.answer("⛔ Доступ запрещён. Команда только для администратора.")
        logger.warning(f"⚠️ Попытка использования /set_manager не-админом: user_id={user_id}")
        return
    
    # Парсим аргументы команды
    args = message.text.split()
    
    if len(args) != 2 or not args[1].isdigit():
        await message.answer(
            text=(
                "❌ <b>Неверный формат команды</b>\n\n"
                "Использование: <code>/set_manager {user_id}</code>\n\n"
                "Пример: <code>/set_manager 123456789</code>"
            ),
            parse_mode="HTML"
        )
        return
    
    target_user_id = int(args[1])
    
    # Проверяем существует ли пользователь
    if not db.user_exists(target_user_id):
        await message.answer(
            text=f"❌ Пользователь с ID <code>{target_user_id}</code> не найден в базе.",
            parse_mode="HTML"
        )
        return
    
    # Назначаем роль менеджера
    if db.set_user_role(target_user_id, 'manager'):
        await message.answer(
            text=(
                f"✅ <b>Роль назначена!</b>\n\n"
                f"👤 Пользователь: <code>{target_user_id}</code>\n"
                f"🎭 Новая роль: <b>MANAGER</b>"
            ),
            parse_mode="HTML"
        )
        
        # Уведомляем пользователя
        try:
            await message.bot.send_message(
                chat_id=target_user_id,
                text=(
                    "🎉 <b>Поздравляем!</b>\n\n"
                    "Вам назначена роль <b>МЕНЕДЖЕРА</b>.\n\n"
                    "Теперь вам доступна команда /staff с расширенными функциями."
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"⚠️ Не удалось уведомить пользователя {target_user_id}: {e}")
    else:
        await message.answer("❌ Ошибка назначения роли. Проверьте логи.")


@router.message(Command("fire_manager"))
async def fire_manager_command(message: types.Message):
    """Снимает роль менеджера (только admin)"""
    user_id = message.from_user.id
    
    # SECURITY: Только admin может снимать менеджеров
    if user_id != config.ADMIN_ID:
        await message.answer("⛔ Доступ запрещён. Команда только для администратора.")
        logger.warning(f"⚠️ Попытка использования /fire_manager не-админом: user_id={user_id}")
        return
    
    # Парсим аргументы команды
    args = message.text.split()
    
    if len(args) != 2 or not args[1].isdigit():
        await message.answer(
            text=(
                "❌ <b>Неверный формат команды</b>\n\n"
                "Использование: <code>/fire_manager {user_id}</code>\n\n"
                "Пример: <code>/fire_manager 123456789</code>"
            ),
            parse_mode="HTML"
        )
        return
    
    target_user_id = int(args[1])
    
    # Проверяем существует ли пользователь
    if not db.user_exists(target_user_id):
        await message.answer(
            text=f"❌ Пользователь с ID <code>{target_user_id}</code> не найден в базе.",
            parse_mode="HTML"
        )
        return
    
    # Снимаем роль менеджера
    if db.set_user_role(target_user_id, 'user'):
        await message.answer(
            text=(
                f"✅ <b>Роль снята!</b>\n\n"
                f"👤 Пользователь: <code>{target_user_id}</code>\n"
                f"🎭 Новая роль: <b>USER</b>"
            ),
            parse_mode="HTML"
        )
        
        # Уведомляем пользователя
        try:
            await message.bot.send_message(
                chat_id=target_user_id,
                text=(
                    "ℹ️ <b>Уведомление</b>\n\n"
                    "Ваша роль менеджера была снята.\n"
                    "Теперь у вас стандартный доступ пользователя."
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"⚠️ Не удалось уведомить пользователя {target_user_id}: {e}")
    else:
        await message.answer("❌ Ошибка изменения роли. Проверьте логи.")


@router.message(Command("list_staff"))
async def list_staff_command(message: types.Message):
    """Показывает список всех менеджеров (только admin)"""
    user_id = message.from_user.id
    
    # SECURITY: Только admin
    if user_id != config.ADMIN_ID:
        await message.answer("⛔ Доступ запрещён.")
        return
    
    try:
        import sqlite3
        conn = sqlite3.connect(db.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, first_name, username, role 
            FROM users 
            WHERE role IN ('manager', 'admin')
            ORDER BY role DESC, user_id
        ''')
        
        staff_list = cursor.fetchall()
        conn.close()
        
        if not staff_list:
            await message.answer("📋 Менеджеров пока нет.")
            return
        
        text = "👥 <b>Список персонала:</b>\n\n"
        
        for user_id, name, username, role in staff_list:
            role_emoji = "👑" if role == "admin" else "👨‍💼"
            username_str = f"@{username}" if username else "нет username"
            text += f"{role_emoji} <b>{role.upper()}</b>\n"
            text += f"├ ID: <code>{user_id}</code>\n"
            text += f"├ Имя: {name or 'Нет имени'}\n"
            text += f"└ Username: {username_str}\n\n"
        
        await message.answer(text, parse_mode="HTML")
        
    except Exception as e:
        await message.answer(f"❌ Ошибка получения списка: {e}")
        logger.error(f"❌ Ошибка в /list_staff: {e}")
