# 🚀 Merix CodeX Bot v3.0 - Deployment Guide

## ✅ Что изменилось в v3.0

### 🔄 Исправлена логика старта
**Правильная последовательность:**
1. `/start` → Проверка пользователя в БД
2. Если нет → Выбор языка
3. Сохранение языка
4. Middleware проверяет подписку на канал
5. Если не подписан → блокировка доступа
6. Если подписан → Главное меню

### 💾 Новая таблица заказов
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    service_name TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### 👤 Обновленный профиль
- **Показывает:** User ID, Balance, Number of Orders
- **Кнопки:**
  - [⚙️ Settings] → [Change Language]
  - [📦 My Orders] → Список заказов со статусами

### 🆘 Раздел помощи
- Текст с инструкциями
- Кнопка: [👨‍💻 Manager] → https://t.me/noxsec

### 🔐 Админ-панель `/admin`
**Скрыта из меню команд (НЕ показывается в set_my_commands)**

**Функции:**
- [📊 Statistics] - Всего пользователей + Новых сегодня
- [📂 Active Orders] - Список заказов (Pending + In Progress)
- [📢 Broadcast] - Рассылка всем пользователям

**Управление заказами:**
- Админ видит список активных заказов
- Клик на заказ → детали
- Может изменить статус:
  - [🔵 В работу] → In Progress
  - [✅ Выполнено] → Done  
  - [❌ Отменить] → Cancelled
- Пользователь получает уведомление об изменении статуса

### 🗑️ Удалено
- ❌ Web App интеграция
- ❌ Реферальная система  
- ❌ Система отзывов
- ❌ `/admin` из меню команд бота

### ✅ Оставлено
- ✅ 4 языка (RU, EN, TJ, UZ)
- ✅ Подписка на канал (middleware)
- ✅ FSM для заказов и рассылки
- ✅ Админ-панель (скрытая)
- ✅ Proxy поддержка для PythonAnywhere

---

## 📦 Деплой на PythonAnywhere

### Шаг 1: Клонирование репозитория

```bash
cd ~
git clone https://github.com/Magasah/merix_CodeX.git
cd merix_CodeX
```

### Шаг 2: Создание виртуального окружения

```bash
# ИСПОЛЬЗУЙТЕ Python 3.11 (НЕ 3.13!)
python3.11 -m venv venv
source venv/bin/activate
```

### Шаг 3: Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Если ошибка с pydantic-core:**
```bash
export PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
pip install -r requirements.txt
```

### Шаг 4: Настройка .env

Создайте файл `.env`:
```bash
nano .env
```

Добавьте:
```env
BOT_TOKEN=8696332583:AAFN9UZsUKhN70XennkstbVtElJunN_oK38
ADMIN_ID=7679557111
CHANNEL_ID=@merix_codex
CHANNEL_URL=https://t.me/merix_codex
PROXY_URL=http://proxy.server:3128
```

**Важно:** Замените `PROXY_URL` на актуальный прокси PythonAnywhere!

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

### Шаг 5: Инициализация базы данных

```bash
python3.11 -c "import database; database.init_db()"
```

Должно вывести: `✅ База данных успешно инициализирована`

### Шаг 6: Проверка настроек

```bash
python3.11 -c "import config; print(f'BOT_TOKEN: {config.BOT_TOKEN[:10]}...'); print(f'ADMIN_ID: {config.ADMIN_ID}'); print(f'CHANNEL_ID: {config.CHANNEL_ID}')"
```

Должно показать ваши данные без ошибок.

### Шаг 7: Запуск бота

```bash
python3.11 main.py
```

**Ожидаемый вывод:**
```
📦 Инициализация базы данных...
✅ База данных успешно инициализирована
============================================================
🤖 Бот Merix CodeX Global v2.0 UPGRADED запущен!
📛 Имя бота: @MerixCodeX_bot
📊 Зарегистрировано роутеров: 8
👨‍💼 ID администратора: 7679557111
📢 Обязательный канал: @merix_codex
🌍 Поддерживаемые языки: Русский, English, Тоҷикӣ, O'zbekcha
============================================================
```

### Шаг 8: Запуск в фоне (screen)

```bash
screen -S merix_bot
python3.11 main.py
```

**Выход из screen:** `Ctrl+A`, потом `D`

**Вернуться к боту:**
```bash
screen -r merix_bot
```

**Остановить бота:** `Ctrl+C`

---

## 🧪 Тестирование

### 1. Проверка команд бота
В Telegram откройте меню бота (/) - должны быть **ТОЛЬКО**:
- `/start` - Restart
- `/help` - Support

❌ `/admin` НЕ должна быть видна!

### 2. Проверка потока старта
1. Новый пользователь нажимает `/start`
2. Показывается выбор языка
3. После выбора → Проверка подписки
4. Если не подписан → блокировка
5. После подписки → Главное меню

### 3. Проверка профиля
1. Нажмите [👤 Профиль]
2. Должны быть кнопки:
   - [⚙️ Настройки]
   - [📦 Мои заказы]
3. [⚙️ Настройки] → [🌐 Изменить язык]
4. [📦 Мои заказы] → "У вас пока нет заказов" (если нет заказов)

### 4. Проверка помощи
1. Нажмите [🆘 Помощь]
2. Должна быть кнопка: [👨‍💻 Менеджер]
3. Клик → открывается https://t.me/noxsec

### 5. Проверка заказа
1. [📂 Услуги] → Выберите услугу
2. [✅ Заказать]
3. Введите описание
4. Подтвердите
5. Админ должен получить уведомление с номером заказа

### 6. Проверка админ-панели
**От админского аккаунта (ADMIN_ID):**
```
/admin
```

Должно показать:
- [📊 Статистика]
- [📂 Активные заказы]
- [📢 Рассылка]

**Тест управления заказами:**
1. [📂 Активные заказы]
2. Выберите заказ
3. Измените статус
4. Пользователь должен получить уведомление

---

## 🔧 Частые проблемы

### Проблема 1: "Module 'reviews' not found"
**Решение:** Файл `handlers/reviews.py` удален, убедитесь что `handlers/__init__.py` НЕ импортирует reviews

### Проблема 2: "Column 'status' does not exist in table orders"
**Решение:** Удалите старую БД и создайте новую:
```bash
rm bot_database.db
python3.11 -c "import database; database.init_db()"
```

### Проблема 3: Бот не отвечает
**Решение:** Проверьте proxy:
```bash
# В .env убедитесь что PROXY_URL правильный
# Или временно удалите PROXY_URL и попробуйте без прокси
```

### Проблема 4: "/admin видна в меню"
**Решение:** Перезапустите бота - команды обновятся автоматически при старте

### Проблема 5: Пользователь не получает уведомление о статусе
**Решение:** Проверьте что:
1. Пользователь не заблокировал бота
2. ADMIN_ID правильный в .env
3. В логах нет ошибок отправки

---

## 📊 Структура БД

### Таблица `users`
```
user_id         INTEGER PRIMARY KEY
username        TEXT
first_name      TEXT
language        TEXT DEFAULT 'ru'
referrer_id     INTEGER
balance         INTEGER DEFAULT 0
created_at      TIMESTAMP
last_interaction TIMESTAMP
```

### Таблица `orders`
```
id              INTEGER PRIMARY KEY AUTOINCREMENT
user_id         INTEGER NOT NULL
service_name    TEXT NOT NULL
description     TEXT NOT NULL
status          TEXT DEFAULT 'Pending'
created_at      TIMESTAMP
```

**Статусы заказов:**
- `Pending` 🟡 - Ожидает
- `In Progress` 🔵 - В работе
- `Done` ✅ - Выполнен
- `Cancelled` ❌ - Отменен

---

## 🔄 Обновление кода на сервере

```bash
cd ~/merix_CodeX
git pull origin main

# Если были изменения в requirements.txt:
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Перезапустите бота:
screen -r merix_bot
# Нажмите Ctrl+C
python3.11 main.py
```

---

## 📝 Проверка логов

```bash
# Просмотр логов в реальном времени:
screen -r merix_bot

# Сохранение логов в файл:
python3.11 main.py > bot.log 2>&1 &

# Просмотр файла логов:
tail -f bot.log
```

---

## 🎯 Итоговый чек-лист

- [ ] Python 3.11 используется (НЕ 3.13)
- [ ] Виртуальное окружение создано
- [ ] Зависимости установлены без ошибок
- [ ] .env настроен с правильными данными
- [ ] База данных инициализирована
- [ ] PROXY_URL настроен (для PythonAnywhere)
- [ ] Бот запускается без ошибок
- [ ] Бот добавлен как админ в канал @merix_codex
- [ ] В меню бота ТОЛЬКО /start и /help
- [ ] /admin работает (скрытая команда)
- [ ] Профиль показывает кнопки Settings и My Orders
- [ ] Помощь показывает кнопку Manager
- [ ] Заказы сохраняются в БД
- [ ] Админ может управлять заказами
- [ ] Пользователь получает уведомления о статусе

---

**Версия:** 3.0 Final  
**Дата:** 31 декабря 2025  
**GitHub:** https://github.com/Magasah/merix_CodeX  
**Статус:** ✅ Production Ready

🎉 **Бот готов к работе на сервере!**
