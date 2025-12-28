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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ База данных успешно инициализирована")
        
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации БД: {e}")
        raise


def add_user(user_id: int, username: Optional[str] = None, 
             first_name: Optional[str] = None, language: str = 'ru') -> bool:
    """
    Добавляет нового пользователя в базу данных
    
    Args:
        user_id: Telegram ID пользователя
        username: Username пользователя (опционально)
        first_name: Имя пользователя (опционально)
        language: Язык интерфейса (по умолчанию 'ru')
        
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
            INSERT INTO users (user_id, username, first_name, language)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, language))
        
        conn.commit()
        conn.close()
        logger.info(f"➕ Добавлен новый пользователь: {user_id}")
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
