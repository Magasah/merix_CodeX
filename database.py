"""
Модуль для работы с базой данных SQLite
Управление пользователями и их настройками
"""
import sqlite3
import logging
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)

# Путь к файлу базы данных
DB_PATH = "bot_database.db"


def init_db():
    """
    Инициализация базы данных
    Создает таблицу users если её не существует
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Создаем таблицу пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                language TEXT DEFAULT 'ru',
                referrer_id INTEGER,
                balance INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Создаем таблицу заказов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                service_name TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Миграция: Добавляем колонку balance если её нет
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'balance' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN balance INTEGER DEFAULT 0')
            logger.info("✅ Добавлена колонка balance в таблицу users")
        
        # Миграция: Добавляем колонку role для RBAC
        if 'role' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN role TEXT DEFAULT "user"')
            logger.info("✅ Добавлена колонка role в таблицу users")
        
        conn.commit()
        conn.close()
        logger.info("✅ База данных успешно инициализирована")
        
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД: {e}")
        raise


def add_user(user_id: int, username: Optional[str] = None, 
             first_name: Optional[str] = None, language: str = 'ru', 
             referrer_id: Optional[int] = None) -> bool:
    """
    Добавляет нового пользователя в базу данных
    
    Args:
        user_id: Telegram ID пользователя
        username: Username пользователя (опционально)
        first_name: Имя пользователя (опционально)
        language: Язык интерфейса (по умолчанию 'ru')
        referrer_id: ID пригласившего пользователя (опционально)
        
    Returns:
        bool: True если пользователь добавлен, False если уже существует
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Проверяем, существует ли пользователь
        cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        if cursor.fetchone():
            conn.close()
            return False
        
        # Добавляем нового пользователя
        cursor.execute('''
            INSERT INTO users (user_id, username, first_name, language, referrer_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, language, referrer_id))
        
        conn.commit()
        conn.close()
        logger.info(f"➕ Добавлен новый пользователь: {user_id} (реферер: {referrer_id})")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка добавления пользователя: {e}")
        return False


def get_user_language(user_id: int) -> Optional[str]:
    """
    Получает язык пользователя из базы данных
    
    Args:
        user_id: Telegram ID пользователя
        
    Returns:
        str: Код языка ('ru', 'en', 'tj', 'uz') или None если пользователь не найден
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения языка пользователя: {e}")
        return None


def update_user_language(user_id: int, language: str) -> bool:
    """
    Обновляет язык пользователя в базе данных
    
    Args:
        user_id: Telegram ID пользователя
        language: Новый код языка
        
    Returns:
        bool: True если обновление успешно
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET language = ?, last_interaction = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (language, user_id))
        
        conn.commit()
        conn.close()
        logger.info(f"🔄 Обновлен язык пользователя {user_id}: {language}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка обновления языка: {e}")
        return False


def update_last_interaction(user_id: int):
    """
    Обновляет время последнего взаимодействия пользователя
    
    Args:
        user_id: Telegram ID пользователя
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET last_interaction = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        logger.error(f"❌ Ошибка обновления взаимодействия: {e}")


def get_user_count() -> int:
    """
    Получает общее количество пользователей в базе
    
    Returns:
        int: Количество пользователей
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения количества пользователей: {e}")
        return 0


def get_all_users() -> List[Tuple[int, str]]:
    """
    Получает список всех пользователей для рассылки
    
    Returns:
        List[Tuple[int, str]]: Список кортежей (user_id, language)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id, language FROM users')
        users = cursor.fetchall()
        
        conn.close()
        return users
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения списка пользователей: {e}")
        return []


def user_exists(user_id: int) -> bool:
    """
    Проверяет, существует ли пользователь в базе
    
    Args:
        user_id: Telegram ID пользователя
        
    Returns:
        bool: True если пользователь существует
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
        
    except Exception as e:
        logger.error(f"❌ Ошибка проверки существования пользователя: {e}")
        return False


def get_users_count_today() -> int:
    """
    Получает количество новых пользователей за сегодня
    
    Returns:
        int: Количество пользователей, зарегистрированных сегодня
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM users 
            WHERE DATE(created_at) = DATE('now')
        ''')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения статистики за сегодня: {e}")
        return 0


def get_users_count() -> int:
    """
    Получает общее количество пользователей
    
    Returns:
        int: Общее количество пользователей
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения общего количества пользователей: {e}")
        return 0


def get_vip_users_count() -> int:
    """
    Получает количество VIP пользователей
    
    Returns:
        int: Количество VIP пользователей
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Проверяем существует ли колонка is_vip
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_vip' in columns:
            cursor.execute('SELECT COUNT(*) FROM users WHERE is_vip = 1')
            count = cursor.fetchone()[0]
        else:
            count = 0
        
        conn.close()
        return count
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения количества VIP пользователей: {e}")
        return 0


def get_user_info(user_id: int) -> Optional[dict]:
    """
    Получает полную информацию о пользователе
    
    Args:
        user_id: Telegram ID пользователя
        
    Returns:
        dict: Словарь с информацией о пользователе или None
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, first_name, language, referrer_id, balance, created_at
            FROM users WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'user_id': result[0],
                'username': result[1],
                'first_name': result[2],
                'language': result[3],
                'referrer_id': result[4],
                'balance': result[5],
                'created_at': result[6]
            }
        return None
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения информации о пользователе: {e}")
        return None


# ============= ФУНКЦИИ ДЛЯ РАБОТЫ С ЗАКАЗАМИ =============

def create_order(user_id: int, service_name: str, description: str) -> Optional[int]:
    """
    Создает новый заказ в базе данных
    
    Args:
        user_id: Telegram ID пользователя
        service_name: Название услуги
        description: Описание заказа
        
    Returns:
        int: ID созданного заказа или None при ошибке
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO orders (user_id, service_name, description, status)
            VALUES (?, ?, ?, 'Pending')
        ''', (user_id, service_name, description))
        
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"📦 Создан новый заказ #{order_id} от пользователя {user_id}")
        return order_id
        
    except Exception as e:
        logger.error(f"❌ Ошибка создания заказа: {e}")
        return None


def get_user_orders(user_id: int) -> List[Tuple]:
    """
    Получает все заказы пользователя
    
    Args:
        user_id: Telegram ID пользователя
        
    Returns:
        List[Tuple]: Список заказов (id, service_name, status, created_at)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, service_name, status, created_at
            FROM orders WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        orders = cursor.fetchall()
        conn.close()
        return orders
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения заказов пользователя: {e}")
        return []


def get_user_orders_count(user_id: int) -> int:
    """
    Получает количество заказов пользователя
    
    Args:
        user_id: Telegram ID пользователя
        
    Returns:
        int: Количество заказов
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM orders WHERE user_id = ?', (user_id,))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
        
    except Exception as e:
        logger.error(f"❌ Ошибка подсчета заказов: {e}")
        return 0


def get_pending_orders() -> List[Tuple]:
    """
    Получает все активные заказы (Pending и In Progress) для админ-панели
    
    Returns:
        List[Tuple]: Список заказов с информацией о пользователе
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT o.id, o.user_id, u.first_name, u.username, 
                   o.service_name, o.description, o.status, o.created_at
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            WHERE o.status IN ('Pending', 'In Progress')
            ORDER BY o.created_at DESC
        ''')
        
        orders = cursor.fetchall()
        conn.close()
        return orders
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения активных заказов: {e}")
        return []


def update_order_status(order_id: int, new_status: str) -> bool:
    """
    Обновляет статус заказа
    
    Args:
        order_id: ID заказа
        new_status: Новый статус ('Pending', 'In Progress', 'Done', 'Cancelled')
        
    Returns:
        bool: True если обновлено успешно
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE orders SET status = ?
            WHERE id = ?
        ''', (new_status, order_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Статус заказа #{order_id} изменен на: {new_status}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка обновления статуса заказа: {e}")
        return False


def get_order_by_id(order_id: int) -> Optional[Tuple]:
    """
    Получает информацию о заказе по ID
    
    Args:
        order_id: ID заказа
        
    Returns:
        Tuple: (id, user_id, service_name, description, status) или None
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, user_id, service_name, description, status
            FROM orders WHERE id = ?
        ''', (order_id,))
        
        order = cursor.fetchone()
        conn.close()
        return order
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения заказа: {e}")
        return None


# ============= ФУНКЦИИ ДЛЯ РАБОТЫ С БАЛАНСОМ =============

def get_user_balance(user_id: int) -> int:
    """
    Получает баланс пользователя
    
    Args:
        user_id: Telegram ID пользователя
        
    Returns:
        int: Баланс пользователя в рублях
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else 0
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения баланса: {e}")
        return 0


def update_user_balance(user_id: int, amount: int) -> bool:
    """
    Обновляет баланс пользователя (добавляет сумму)
    
    Args:
        user_id: Telegram ID пользователя
        amount: Сумма для добавления (может быть отрицательной)
        
    Returns:
        bool: True если успешно обновлено
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET balance = balance + ?
            WHERE user_id = ?
        ''', (amount, user_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"💰 Баланс пользователя {user_id} изменён на {amount} RUB")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка обновления баланса: {e}")
        return False


def set_user_balance(user_id: int, balance: int) -> bool:
    """
    Устанавливает баланс пользователя (заменяет текущий)
    
    Args:
        user_id: Telegram ID пользователя
        balance: Новый баланс
        
    Returns:
        bool: True если успешно установлено
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET balance = ?
            WHERE user_id = ?
        ''', (balance, user_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"💰 Баланс пользователя {user_id} установлен: {balance} RUB")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка установки баланса: {e}")
        return False


# ============= RBAC: УПРАВЛЕНИЕ РОЛЯМИ =============

def get_user_role(user_id: int) -> str:
    """
    Получает роль пользователя
    
    Args:
        user_id: Telegram ID пользователя
        
    Returns:
        str: Роль пользователя ('user', 'manager', 'admin')
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT role FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else 'user'
        
    except Exception as e:
        logger.error(f"❌ Ошибка получения роли: {e}")
        return 'user'


def set_user_role(user_id: int, role: str) -> bool:
    """
    Устанавливает роль пользователя
    
    Args:
        user_id: Telegram ID пользователя
        role: Новая роль ('user', 'manager', 'admin')
        
    Returns:
        bool: True если успешно установлено
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET role = ?
            WHERE user_id = ?
        ''', (role, user_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"👤 Роль пользователя {user_id} изменена на: {role}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка установки роли: {e}")
        return False


def has_permission(user_id: int, required_role: str) -> bool:
    """
    Проверяет имеет ли пользователь необходимый уровень доступа
    
    Иерархия: user < manager < admin
    
    Args:
        user_id: Telegram ID пользователя
        required_role: Требуемая роль ('user', 'manager', 'admin')
        
    Returns:
        bool: True если доступ разрешён
    """
    import config
    
    # ADMIN_ID всегда имеет admin права
    if user_id == config.ADMIN_ID:
        return True
    
    user_role = get_user_role(user_id)
    
    roles_hierarchy = {'user': 0, 'manager': 1, 'admin': 2}
    
    user_level = roles_hierarchy.get(user_role, 0)
    required_level = roles_hierarchy.get(required_role, 0)
    
    return user_level >= required_level
