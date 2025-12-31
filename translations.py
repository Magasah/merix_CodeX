"""
Модуль переводов для многоязычной поддержки
Поддерживаемые языки: Русский, English, Тоҷикӣ, O'zbekcha
"""

# Словарь всех переводов
TRANSLATIONS = {
    # ============= РУССКИЙ =============
    'ru': {
        # Подписка на канал
        'subscription_required': (
            '⚠️ <b>Для использования бота необходимо подписаться на наш канал</b>\n\n'
            'Подпишитесь на канал <b>Merix CodeX</b>, чтобы получить доступ ко всем функциям бота.\n\n'
            '👇 Нажмите кнопку ниже для подписки:'
        ),
        'btn_subscribe': '🔗 Подписаться на канал',
        'btn_check_subscription': '✅ Я подписался',
        'please_subscribe': 'Пожалуйста, сначала подпишитесь на канал!',
        'subscription_confirmed': 'Спасибо за подписку!',
        
        # Выбор языка
        'choose_language': '🌍 <b>Выберите язык / Choose language</b>\n\nВыберите предпочитаемый язык для общения с ботом:',
        'language_set': '✅ Язык успешно установлен: <b>Русский</b>',
        'menu_updated': '🔄 <b>Главное меню обновлено</b>',
        
        # Кнопки главного меню
        'btn_services': '📂 Услуги',
        'btn_profile': '👤 Профиль',
        'btn_help': '🆘 Помощь',
        'btn_about': 'ℹ️ О компании',
        
        # Приветствие
        'welcome': (
            '👋 Здравствуйте, <b>{name}</b>!\n\n'
            'Добро пожаловать в <b>Merix CodeX</b> — профессиональное IT-агентство '
            'с круглосуточной поддержкой.\n\n'
            '🔹 <b>Наши услуги:</b>\n'
            '  • Разработка Telegram ботов\n'
            '  • Создание современных веб-сайтов\n'
            '  • Аудит безопасности и пентест\n\n'
            '⏰ <b>Поддержка 24/7</b>\n'
            '📱 Используйте меню ниже для навигации.'
        ),
        
        # Услуги
        'services_title': '<b>📂 Выберите категорию услуг:</b>\n\nВсе цены обсуждаются индивидуально в зависимости от сложности проекта.',
        'btn_bots': '🤖 Telegram Боты',
        'btn_websites': '🌐 Веб-сайты',
        'btn_security': '🛡️ Безопасность',
        'btn_fast_start': '📦 Пакет "Быстрый старт"',
        'btn_ai_automation': '🤖 AI Автоматизация',
        'btn_tech_support': '🛡️ Тех. поддержка',
        'btn_back': '🔙 Назад',
        'btn_order': '✅ Заказать',
        
        'service_bots': (
            '<b>🤖 Разработка Telegram ботов</b>\n\n'
            '💰 <b>Стоимость:</b> от 200 TJS / 1800 RUB\n'
            '<i>Цена зависит от сложности и функционала</i>\n\n'
            '✨ <b>Что входит:</b>\n'
            '  • Разработка с нуля или доработка\n'
            '  • Интеграция с базами данных\n'
            '  • Админ-панель управления\n'
            '  • Техническая поддержка\n\n'
            '📋 <b>Официальный договор предоставляется</b>\n'
            '⏱ Срок: от 5 рабочих дней'
        ),
        
        'service_websites': (
            '<b>🌐 Создание веб-сайтов</b>\n\n'
            '💼 <b>Лендинги и корпоративные сайты</b>\n'
            '<i>Цена обсуждается индивидуально</i>\n\n'
            '✨ <b>Что входит:</b>\n'
            '  • Современный адаптивный дизайн\n'
            '  • SEO-оптимизация\n'
            '  • Интеграция с CRM\n'
            '  • Система управления контентом\n\n'
            '📋 <b>Официальный договор предоставляется</b>\n'
            '⏱ Срок: от 10 рабочих дней'
        ),
        
        'service_security': (
            '<b>🛡️ Информационная безопасность</b>\n\n'
            '🔒 <b>Базовый аудит и защита</b>\n'
            '<i>Цена обсуждается индивидуально по проекту</i>\n\n'
            '✨ <b>Что входит:</b>\n'
            '  • Аудит безопасности приложений\n'
            '  • Поиск уязвимостей (пентест)\n'
            '  • Рекомендации по защите\n'
            '  • Настройка систем мониторинга\n\n'
            '📋 <b>Официальный договор предоставляется</b>\n'
            '<i>Мы не пугаем высокими ценами — все обсуждается индивидуально</i>'
        ),
        
        'service_fast_start': (
            '<b>📦 Пакет "Быстрый старт"</b>\n\n'
            '💰 <b>Стоимость:</b> от 700 TJS\n'
            '<i>Landing + Bot + Дизайн канала</i>\n\n'
            '✨ <b>Что входит:</b>\n'
            '  • Одностраничный лендинг\n'
            '  • Telegram бот с базовыми функциями\n'
            '  • Дизайн для вашего канала\n'
            '  • Настройка домена и хостинга\n\n'
            '📋 <b>Официальный договор предоставляется</b>\n'
            '⏱ Срок: 7-10 рабочих дней'
        ),
        
        # Алиасы для совместимости
        'service_package': (
            '<b>📦 Пакет «Быстрый старт»</b>\n\n'
            'Входит: Сайт-визитка + Telegram-бот + Оформление канала.\n\n'
            '💰 <b>Цена:</b> от 700 TJS'
        ),
        
        'service_ai_automation': (
            '<b>🤖 AI Автоматизация</b>\n\n'
            '💰 <b>Стоимость:</b> от 400 TJS\n'
            '<i>Кастомный AI-ассистент для бизнеса</i>\n\n'
            '✨ <b>Что входит:</b>\n'
            '  • Интеграция с ChatGPT/Claude\n'
            '  • Обучение на ваших данных\n'
            '  • Автоматизация рутинных задач\n'
            '  • Поддержка нескольких языков\n\n'
            '📋 <b>Официальный договор предоставляется</b>\n'
            '⏱ Срок: 5-7 рабочих дней'
        ),
        
        'service_ai': (
            '<b>🤖 AI-Автоматизация</b>\n\n'
            'Внедрение умного ассистента, который знает всё о вашем товаре и отвечает клиентам 24/7.\n\n'
            '💰 <b>Цена:</b> от 400 TJS'
        ),
        
        'service_tech_support': (
            '<b>🛡️ Техническая поддержка 24/7</b>\n\n'
            '💰 <b>Стоимость:</b> 150 TJS/месяц\n'
            '<i>Мониторинг и защита ваших систем</i>\n\n'
            '✨ <b>Что входит:</b>\n'
            '  • Круглосуточный мониторинг\n'
            '  • Оперативное устранение проблем\n'
            '  • Регулярные обновления\n'
            '  • Резервное копирование данных\n\n'
            '📋 <b>Официальный договор предоставляется</b>\n'
            '💳 Ежемесячная оплата'
        ),
        
        'service_tech': (
            '<b>🛡️ Техподдержка</b>\n\n'
            'Мониторинг 24/7, обновление бота, защита от атак и сбоев.\n\n'
            '💰 <b>Цена:</b> 150 TJS / мес.'
        ),
        
        # Профиль
        'profile_text': (
            '👤 <b>Ваш профиль</b>\n\n'
            '📋 <b>Информация:</b>\n'
            '• ID: <code>{user_id}</code>\n'
            '• Имя: {name}\n'
            '• Username: {username}\n'
            '• Язык: 🇷🇺 Русский\n\n'
            '💰 <b>Баланс:</b> {balance} TJS\n'
            '📦 <b>Всего заказов:</b> {orders_count}\n\n'
            'Используйте кнопки ниже для управления профилем:'
        ),
        'btn_settings': '⚙️ Настройки',
        'btn_my_orders': '📦 Мои заказы',
        'btn_change_language': '🌐 Изменить язык',
        'no_orders': '📦 <b>У вас пока нет заказов</b>\n\nПерейдите в <b>📂 Услуги</b> для оформления заказа.',
        'my_orders_title': '📦 <b>Ваши заказы</b>\n\n',
        
        # О компании
        'about_text': (
            'ℹ️ <b>О компании Merix CodeX</b>\n\n'
            '<b>Merix CodeX</b> — команда профессиональных IT-специалистов.\n\n'
            '🎯 <b>Наша миссия:</b>\n'
            'Предоставлять качественные технологические решения для бизнеса.\n\n'
            '💡 <b>Преимущества:</b>\n'
            '  • Поддержка 24/7\n'
            '  • Официальные договора\n'
            '  • Индивидуальный подход\n'
            '  • Гибкие цены\n\n'
            '� <b>Instagram:</b> https://instagram.com/merix_codex\n\n'
            '�📞 Для консультации используйте <b>«🆘 Помощь»</b>'
        ),
        
        # Помощь
        'help_text': (
            '🆘 <b>Поддержка 24/7</b>\n\n'
            '<b>Как сделать заказ?</b>\n'
            '1. Перейдите в <b>📂 Услуги</b>\n'
            '2. Выберите категорию\n'
            '3. Нажмите <b>✅ Заказать</b>\n'
            '4. Опишите вашу задачу\n\n'
            '<b>Нужна консультация?</b>\n'
            'Свяжитесь с нашим менеджером напрямую, нажав кнопку ниже.\n\n'
            '⏰ Мы всегда на связи!'
        ),
        'btn_manager': '👨‍💻 Менеджер',
        
        # Заказ
        'order_description': (
            '📝 <b>Оформление заказа: {service}</b>\n\n'
            'Пожалуйста, опишите подробно вашу задачу:\n\n'
            '• Какой функционал необходим?\n'
            '• Есть ли примеры?\n'
            '• Какие сроки?\n\n'
            'Чем подробнее описание, тем точнее оценка.'
        ),
        'order_confirmation': (
            '✅ <b>Проверьте вашу заявку</b>\n\n'
            '<b>Услуга:</b> {service}\n\n'
            '<b>Описание:</b>\n{description}\n\n'
            'Если всё верно, нажмите <b>«✅ Отправить»</b>.'
        ),
        'btn_send': '✅ Отправить',
        'btn_cancel': '❌ Отменить',
        'order_sent': (
            '✅ <b>Заявка успешно отправлена!</b>\n\n'
            'Наш менеджер свяжется с вами в ближайшее время.\n\n'
            '⏰ Среднее время ответа: 1-2 часа'
        ),
        'order_cancelled': '❌ <b>Заявка отменена</b>\n\nВы можете оформить новую заявку в любое время.',
        'order_error': '❌ <b>Ошибка отправки заявки</b>\n\nПопробуйте позже или свяжитесь напрямую через <b>🆘 Помощь</b>.',
        
        # Админ уведомление
        'admin_new_order': (
            '🔔 <b>Новая заявка!</b>\n\n'
            '<b>Услуга:</b> {service}\n\n'
            '👤 <b>Клиент:</b> {name}\n'
            '📱 <b>Username:</b> {username}\n'
            '🆔 <b>ID:</b> <code>{user_id}</code>\n'
            '🌐 <b>Язык:</b> {language}\n\n'
            '<b>Описание:</b>\n{description}'
        ),
        
        # Отзывы
        'reviews_menu': '⭐ <b>Отзывы</b>\n\nВыберите действие:',
        'btn_read_reviews': '📖 Читать отзывы',
        'btn_write_review': '✍️ Написать отзыв',
        'review_prompt': '✍️ <b>Написать отзыв</b>\n\nНапишите ваш отзыв о нашей работе. После модерации он будет опубликован в канале.',
        'review_sent': '✅ <b>Спасибо за отзыв!</b>\n\nВаш отзыв отправлен на модерацию и скоро будет опубликован.',
        'review_to_admin': '⭐ <b>Новый отзыв от пользователя</b>\n\n👤 <b>От:</b> {name} (@{username})\n🆔 <b>ID:</b> <code>{user_id}</code>\n\n<b>Отзыв:</b>\n{review}',
        
        # Статусы заказов
        'order_status_pending': '🟡 Ожидает',
        'order_status_in_progress': '🔵 В работе',
        'order_status_done': '✅ Выполнен',
        'order_status_cancelled': '❌ Отменен',
        'order_status_changed': '📬 <b>Статус вашего заказа изменен</b>\n\n📦 Заказ #{order_id}: {service}\n🔄 Новый статус: {status}',
        
        # Админ-панель
        'admin_panel': '🔐 <b>Админ-панель</b>\n\nВыберите действие:',
        'btn_statistics': '📊 Статистика',
        'btn_broadcast': '📢 Рассылка',
        'btn_active_orders': '📂 Активные заказы',
        'statistics_text': '📊 <b>Статистика бота</b>\n\n👥 Всего пользователей: <b>{total}</b>\n📅 Новых сегодня: <b>{today}</b>',
        'no_active_orders': '📂 <b>Нет активных заказов</b>\n\nВсе заказы обработаны.',
        'active_orders_title': '📂 <b>Активные заказы</b>\n\nВыберите заказ для управления:',
        'order_details': (
            '📦 <b>Заказ #{order_id}</b>\n\n'
            '👤 <b>Клиент:</b> {name} (@{username})\n'
            '🆔 <b>ID:</b> <code>{user_id}</code>\n\n'
            '🛠 <b>Услуга:</b> {service}\n'
            '📝 <b>Описание:</b>\n{description}\n\n'
            '🔄 <b>Текущий статус:</b> {status}'
        ),
        'btn_set_working': '🔵 В работу',
        'btn_set_done': '✅ Выполнено',
        'btn_set_cancelled': '❌ Отменить',
        'broadcast_prompt': '📢 <b>Рассылка сообщения</b>\n\nОтправьте сообщение, которое хотите разослать всем пользователям:',
        'broadcast_success': '✅ <b>Рассылка завершена</b>\n\n📤 Отправлено: {success}\n❌ Ошибок: {failed}',
        'not_admin': '❌ У вас нет доступа к этой команде.',
    },
    
    # ============= ENGLISH =============
    'en': {
        # Channel subscription
        'subscription_required': (
            '⚠️ <b>To use this bot, please subscribe to our channel</b>\n\n'
            'Subscribe to <b>Merix CodeX</b> channel to get access to all bot features.\n\n'
            '👇 Click the button below to subscribe:'
        ),
        'btn_subscribe': '🔗 Subscribe to channel',
        'btn_check_subscription': '✅ I subscribed',
        'please_subscribe': 'Please subscribe to the channel first!',
        
        'choose_language': '🌍 <b>Choose language / Выберите язык</b>\n\nSelect your preferred language:',
        'language_set': '✅ Language successfully set: <b>English</b>',
        'menu_updated': '🔄 <b>Main menu updated</b>',
        
        'btn_services': '📂 Services',
        'btn_profile': '👤 Profile',
        'btn_help': '🆘 Help',
        'btn_about': 'ℹ️ About Us',
        
        'welcome': (
            '👋 Hello, <b>{name}</b>!\n\n'
            'Welcome to <b>Merix CodeX</b> — a professional IT agency '
            'with 24/7 support.\n\n'
            '🔹 <b>Our services:</b>\n'
            '  • Telegram bot development\n'
            '  • Modern website creation\n'
            '  • Security audit & pentesting\n\n'
            '⏰ <b>24/7 Support</b>\n'
            '📱 Use the menu below for navigation.'
        ),
        
        'services_title': '<b>📂 Choose a service category:</b>\n\nAll prices are negotiable depending on project complexity.',
        'btn_bots': '🤖 Telegram Bots',
        'btn_websites': '🌐 Websites',
        'btn_security': '🛡️ Security',
        'btn_back': '🔙 Back',
        'btn_order': '✅ Order',
        
        'service_bots': (
            '<b>🤖 Telegram Bot Development</b>\n\n'
            '💰 <b>Price:</b> from 200 TJS / 1800 RUB\n'
            '<i>Price depends on complexity and features</i>\n\n'
            '✨ <b>Included:</b>\n'
            '  • Development from scratch or improvements\n'
            '  • Database integration\n'
            '  • Admin panel\n'
            '  • Technical support\n\n'
            '📋 <b>Official contract provided</b>\n'
            '⏱ Timeline: from 5 business days'
        ),
        
        'service_websites': (
            '<b>🌐 Website Development</b>\n\n'
            '💼 <b>Landing pages & Corporate sites</b>\n'
            '<i>Price negotiable individually</i>\n\n'
            '✨ <b>Included:</b>\n'
            '  • Modern responsive design\n'
            '  • SEO optimization\n'
            '  • CRM integration\n'
            '  • Content management system\n\n'
            '📋 <b>Official contract provided</b>\n'
            '⏱ Timeline: from 10 business days'
        ),
        
        'service_security': (
            '<b>🛡️ Information Security</b>\n\n'
            '🔒 <b>Basic audit & protection</b>\n'
            '<i>Price discussed individually per project</i>\n\n'
            '✨ <b>Included:</b>\n'
            '  • Application security audit\n'
            '  • Vulnerability assessment (pentest)\n'
            '  • Security recommendations\n'
            '  • Monitoring system setup\n\n'
            '📋 <b>Official contract provided</b>\n'
            '<i>We don\'t scare with high prices — everything is discussed individually</i>'
        ),
        
        'service_package': (
            '<b>📦 "Fast Start" Package</b>\n\n'
            'Includes: Landing page + Telegram bot + Channel design.\n\n'
            '💰 <b>Price:</b> from 700 TJS'
        ),
        
        'service_ai': (
            '<b>🤖 AI Automation</b>\n\n'
            'Smart assistant implementation that knows everything about your product and responds to customers 24/7.\n\n'
            '💰 <b>Price:</b> from 400 TJS'
        ),
        
        'service_tech': (
            '<b>🛡️ Tech Support</b>\n\n'
            '24/7 monitoring, bot updates, protection from attacks and failures.\n\n'
            '💰 <b>Price:</b> 150 TJS / month'
        ),
        
        'profile_text': (
            '👤 <b>Your Profile</b>\n\n'
            '<b>Name:</b> {name}\n'
            '<b>Username:</b> {username}\n'
            '<b>ID:</b> <code>{user_id}</code>\n'
            '<b>Language:</b> 🇺🇸 English\n\n'
            '🌟 You are a valued client of Merix CodeX!\n\n'
            '💼 To order, go to <b>«📂 Services»</b>'
        ),
        
        'about� <b>Instagram:</b> https://instagram.com/merix_codex\n\n'
            '�_text': (
            'ℹ️ <b>About Merix CodeX</b>\n\n'
            '<b>Merix CodeX</b> — a team of professional IT specialists.\n\n'
            '🎯 <b>Our mission:</b>\n'
            'Providing quality technology solutions for business.\n\n'
            '💡 <b>Advantages:</b>\n'
            '  • 24/7 Support\n'
            '  • Official contracts\n'
            '  • Individual approach\n'
            '  • Flexible pricing\n\n'
            '📞 For consultation use <b>«🆘 Help»</b>'
        ),
        
        'help_text': (
            '🆘 <b>24/7 Support</b>\n\n'
            '<b>How to order?</b>\n'
            '1. Go to <b>📂 Services</b>\n'
            '2. Choose a category\n'
            '3. Click <b>✅ Order</b>\n'
            '4. Describe your task\n\n'
            '<b>Need help?</b>\n'
            '👨‍💼 Contact our manager:\n'
            '{admin_link}\n\n'
            '⏰ We are always available!'
        ),
        
        'order_description': (
            '📝 <b>Ordering: {service}</b>\n\n'
            'Please describe your task in detail:\n\n'
            '• What features are needed?\n'
            '• Any examples?\n'
            '• Timeline?\n\n'
            'More details = more accurate estimate.'
        ),
        'order_confirmation': (
            '✅ <b>Check your request</b>\n\n'
            '<b>Service:</b> {service}\n\n'
            '<b>Description:</b>\n{description}\n\n'
            'If correct, click <b>«✅ Send»</b>.'
        ),
        'btn_send': '✅ Send',
        'btn_cancel': '❌ Cancel',
        'order_sent': (
            '✅ <b>Request sent successfully!</b>\n\n'
            'Our manager will contact you shortly.\n\n'
            '⏰ Average response time: 1-2 hours'
        ),
        'order_cancelled': '❌ <b>Request cancelled</b>\n\nYou can create a new request anytime.',
        'order_error': '❌ <b>Error sending request</b>\n\nTry later or contact directly via <b>🆘 Help</b>.',
        
        'admin_new_order': (
            '🔔 <b>New order!</b>\n\n'
            '<b>Service:</b> {service}\n\n'
            '👤 <b>Client:</b> {name}\n'
            '📱 <b>Username:</b> {username}\n'
            '🆔 <b>ID:</b> <code>{user_id}</code>\n'
            '🌐 <b>Language:</b> {language}\n\n'
            '<b>Description:</b>\n{description}'
        ),
        
        'admin_panel': '🔐 <b>Admin Panel</b>\n\nChoose action:',
        'btn_statistics': '📊 Statistics',
        'btn_broadcast': '📢 Broadcast',
        'statistics_text': '📊 <b>Bot Statistics</b>\n\n👥 Total users: <b>{count}</b>',
        'broadcast_prompt': '📢 <b>Broadcast message</b>\n\nSend the message you want to broadcast to all users:',
        'broadcast_success': '✅ <b>Broadcast completed</b>\n\n📤 Sent: {success}\n❌ Failed: {failed}',
        'not_admin': '❌ You don\'t have access to this command.',
    },
    
    # ============= ТОҶИКӢ =============
    'tj': {
        # Обуна ба канал
        'subscription_required': (
            '⚠️ <b>Барои истифодаи бот ба каналамон обуна шавед</b>\n\n'
            'Ба канали <b>Merix CodeX</b> обуна шавед то ба ҳамаи имкониятҳои бот дастрасӣ пайдо кунед.\n\n'
            '👇 Барои обуна тугмаи поёнро пахш кунед:'
        ),
        'btn_subscribe': '🔗 Обуна шудан ба канал',
        'btn_check_subscription': '✅ Ман обуна шудам',
        'please_subscribe': 'Лутфан аввал ба канал обуна шавед!',
        
        'choose_language': '🌍 <b>Интихоби забон / Choose language</b>\n\nЗабони дилхоҳро интихоб кунед:',
        'language_set': '✅ Забон муваффақона танзим шуд: <b>Тоҷикӣ</b>',
        'menu_updated': '🔄 <b>Менюи асосӣ навсозӣ шуд</b>',
        
        'btn_services': '📂 Хизматрасонӣ',
        'btn_profile': '👤 Профил',
        'btn_help': '🆘 Кӯмак',
        'btn_about': 'ℹ️ Дар бораи мо',
        
        'welcome': (
            '👋 Салом, <b>{name}</b>!\n\n'
            'Хуш омадед ба <b>Merix CodeX</b> — агентии касбии IT '
            'бо дастгирии шабонарӯзӣ.\n\n'
            '🔹 <b>Хизматрасонии мо:</b>\n'
            '  • Таҳияи ботҳои Telegram\n'
            '  • Сохтани сомонаҳои муосир\n'
            '  • Аудити бехатарӣ ва пентест\n\n'
            '⏰ <b>Дастгирӣ 24/7</b>\n'
            '📱 Барои навигатсия менюи поёнро истифода баред.'
        ),
        
        'services_title': '<b>📂 Категорияи хизматро интихоб кунед:</b>\n\nҲамаи нархҳо вобаста ба мураккабии лоиҳа баррасӣ мешаванд.',
        'btn_bots': '🤖 Ботҳои Telegram',
        'btn_websites': '🌐 Сомонаҳо',
        'btn_security': '🛡️ Бехатарӣ',
        'btn_back': '🔙 Бозгашт',
        'btn_order': '✅ Фармоиш',
        
        'service_bots': (
            '<b>🤖 Таҳияи ботҳои Telegram</b>\n\n'
            '💰 <b>Нарх:</b> аз 200 сомонӣ / 1800 рубл\n'
            '<i>Нарх вобаста ба мураккабӣ ва функсионал</i>\n\n'
            '✨ <b>Дар бар мегирад:</b>\n'
            '  • Таҳия аз сифр ё такмил\n'
            '  • Пайваст ба базаи додаҳо\n'
            '  • Панели админ\n'
            '  • Дастгирии техникӣ\n\n'
            '📋 <b>Шартномаи расмӣ пешниҳод мешавад</b>\n'
            '⏱ Мӯҳлат: аз 5 рӯзи корӣ'
        ),
        
        'service_websites': (
            '<b>🌐 Сохтани сомонаҳо</b>\n\n'
            '💼 <b>Лендингҳо ва сомонаҳои корпоративӣ</b>\n'
            '<i>Нарх ба таври инфиродӣ баррасӣ мешавад</i>\n\n'
            '✨ <b>Дар бар мегирад:</b>\n'
            '  • Дизайни муосири мутобиқшаванда\n'
            '  • Оптимизатсияи SEO\n'
            '  • Пайваст ба CRM\n'
            '  • Системаи идораи мундариҷа\n\n'
            '📋 <b>Шартномаи расмӣ пешниҳод мешавад</b>\n'
            '⏱ Мӯҳлат: аз 10 рӯзи корӣ'
        ),
        
        'service_security': (
            '<b>🛡️ Бехатарии иттилоотӣ</b>\n\n'
            '🔒 <b>Аудити асосӣ ва ҳифозат</b>\n'
            '<i>Нарх барои ҳар лоиҳа ба таври инфиродӣ баррасӣ мешавад</i>\n\n'
            '✨ <b>Дар бар мегирад:</b>\n'
            '  • Аудити бехатарии барномаҳо\n'
            '  • Ҷустуҷӯи осебпазирӣ (пентест)\n'
            '  • Тавсияҳо оид ба ҳифозат\n'
            '  • Танзими системаи мониторинг\n\n'
            '📋 <b>Шартномаи расмӣ пешниҳод мешавад</b>\n'
            '<i>Мо бо нархҳои баланд натарсонем — ҳама чиз ба таври инфиродӣ баррасӣ мешавад</i>'
        ),
        
        'service_package': (
            '<b>📦 Бастаи «Оғози зуд»</b>\n\n'
            'Дар бар мегирад: Сайт-визитка + Telegram-бот + Тарҳи канал.\n\n'
            '💰 <b>Нарх:</b> аз 700 сомонӣ'
        ),
        
        'service_ai': (
            '<b>🤖 AI-Автоматизатсия</b>\n\n'
            'Ёвари ҳушманд, ки дар бораи моли шумо ҳама чизро медонад ва ба мизоҷон 24/7 ҷавоб медиҳад.\n\n'
            '💰 <b>Нарх:</b> аз 400 сомонӣ'
        ),
        
        'service_tech': (
            '<b>🛡️ Дастгирии техникӣ</b>\n\n'
            'Назорат 24/7, навсозии бот, муҳофизат аз ҳамлаҳо.\n\n'
            '💰 <b>Нарх:</b> 150 сомонӣ / моҳ'
        ),
        
        'profile_text': (
            '👤 <b>Профили шумо</b>\n\n'
            '<b>Ном:</b> {name}\n'
            '<b>Номи корбар:</b> {username}\n'
            '<b>ID:</b> <code>{user_id}</code>\n'
            '<b>Забон:</b> 🇹🇯 Тоҷикӣ\n\n'
            '🌟 Шумо муштарии арзишманди Merix CodeX ҳастед!\n\n'
            '💼 Барои фармоиш ба <b>«📂 Хизматрасонӣ»</b> гузаред'
        ),
        
        'about_text': (
            'ℹ️ <b>Дар бораи Merix CodeX</b>\n\n'
            '<b>Merix CodeX</b> — дастаи мутахассисони касбии IT.\n\n'
            '🎯 <b>Мақсади мо:</b>\n'
            'Пешниҳоди роҳҳалҳои технологии сифатӣ барои бизнес.\n\n'
            '💡 <b>Бартарияҳо:</b>\n'
            '  • Дастгирии 24/7\n'
            '  • Шартномаҳои расмӣ\n'
            '  • Равиши инфиродӣ\n'
            '  • Нархҳои чандир\n\n'
            '� <b>Instagram:</b> https://instagram.com/merix_codex\n\n'
            '�📞 Барои маслиҳат аз <b>«🆘 Кӯмак»</b> истифода баред'
        ),
        
        'help_text': (
            '🆘 <b>Дастгирии 24/7</b>\n\n'
            '<b>Чӣ тавр фармоиш диҳам?</b>\n'
            '1. Ба <b>📂 Хизматрасонӣ</b> гузаред\n'
            '2. Категорияро интихоб кунед\n'
            '3. <b>✅ Фармоиш</b>-ро пахш кунед\n'
            '4. Вазифаи худро тавсиф кунед\n\n'
            '<b>Кӯмак лозим аст?</b>\n'
            '👨‍💼 Бо менеҷери мо тамос гиред:\n'
            '{admin_link}\n\n'
            '⏰ Мо ҳамеша дар дастрас ҳастем!'
        ),
        
        'order_description': (
            '📝 <b>Фармоиш: {service}</b>\n\n'
            'Лутфан вазифаи худро муфассал тавсиф кунед:\n\n'
            '• Кадом функсионал лозим аст?\n'
            '• Намунаҳо ҳастанд?\n'
            '• Мӯҳлатҳо?\n\n'
            'Ҳар чӣ муфассалтар тавсиф = баҳодиҳии дақиқтар.'
        ),
        'order_confirmation': (
            '✅ <b>Дархости худро санҷед</b>\n\n'
            '<b>Хизмат:</b> {service}\n\n'
            '<b>Тавсиф:</b>\n{description}\n\n'
            'Агар дуруст бошад, <b>«✅ Фиристодан»</b>-ро пахш кунед.'
        ),
        'btn_send': '✅ Фиристодан',
        'btn_cancel': '❌ Бекор кардан',
        'order_sent': (
            '✅ <b>Дархост муваффақона фиристода шуд!</b>\n\n'
            'Менеҷери мо ба зудӣ бо шумо тамос мегирад.\n\n'
            '⏰ Вақти миёнаи ҷавоб: 1-2 соат'
        ),
        'order_cancelled': '❌ <b>Дархост бекор карда шуд</b>\n\nШумо метавонед дархости навро дар ҳар вақт эҷод кунед.',
        'order_error': '❌ <b>Хатои фиристодани дархост</b>\n\nБаъдтар кӯшиш кунед ё бевосита тавассути <b>🆘 Кӯмак</b> тамос гиред.',
        
        'admin_new_order': (
            '🔔 <b>Дархости нав!</b>\n\n'
            '<b>Хизмат:</b> {service}\n\n'
            '👤 <b>Муштарӣ:</b> {name}\n'
            '📱 <b>Номи корбар:</b> {username}\n'
            '🆔 <b>ID:</b> <code>{user_id}</code>\n'
            '🌐 <b>Забон:</b> {language}\n\n'
            '<b>Тавсиф:</b>\n{description}'
        ),
        
        'admin_panel': '🔐 <b>Панели админ</b>\n\nАмалро интихоб кунед:',
        'btn_statistics': '📊 Омор',
        'btn_broadcast': '📢 Паҳнкунӣ',
        'statistics_text': '📊 <b>Омори бот</b>\n\n👥 Ҳамагӣ корбарон: <b>{count}</b>',
        'broadcast_prompt': '📢 <b>Паҳнкунии паём</b>\n\nПаёме, ки мехоҳед ба ҳамаи корбарон фиристед, ирсол кунед:',
        'broadcast_success': '✅ <b>Паҳнкунӣ анҷом ёфт</b>\n\n📤 Фиристода шуд: {success}\n❌ Хатоҳо: {failed}',
        'not_admin': '❌ Шумо ба ин фармон дастрасӣ надоред.',
    },
    
    # ============= O'ZBEKCHA =============
    'uz': {
        # Kanalga obuna
        'subscription_required': (
            '⚠️ <b>Botdan foydalanish uchun kanalimizga obuna bo\'ling</b>\n\n'
            '<b>Merix CodeX</b> kanaliga obuna bo\'ling va barcha imkoniyatlardan foydalaning.\n\n'
            '👇 Obuna bo\'lish uchun quyidagi tugmani bosing:'
        ),
        'btn_subscribe': '🔗 Kanalga obuna bo\'lish',
        'btn_check_subscription': '✅ Men obuna bo\'ldim',
        'please_subscribe': 'Iltimos, avval kanalga obuna bo\'ling!',
        
        'choose_language': '🌍 <b>Tilni tanlang / Choose language</b>\n\nKerakli tilni tanlang:',
        'language_set': '✅ Til muvaffaqiyatli o\'rnatildi: <b>O\'zbekcha</b>',
        'menu_updated': '🔄 <b>Asosiy menyu yangilandi</b>',
        
        'btn_services': '📂 Xizmatlar',
        'btn_profile': '👤 Profil',
        'btn_help': '🆘 Yordam',
        'btn_about': 'ℹ️ Biz haqimizda',
        
        'welcome': (
            '👋 Salom, <b>{name}</b>!\n\n'
            '<b>Merix CodeX</b>ga xush kelibsiz — 24/7 qo\'llab-quvvatlash '
            'bilan professional IT agentligi.\n\n'
            '🔹 <b>Bizning xizmatlar:</b>\n'
            '  • Telegram botlarni ishlab chiqish\n'
            '  • Zamonaviy veb-saytlar yaratish\n'
            '  • Xavfsizlik auditi va pentest\n\n'
            '⏰ <b>24/7 Qo\'llab-quvvatlash</b>\n'
            '📱 Navigatsiya uchun quyidagi menyudan foydalaning.'
        ),
        
        'services_title': '<b>📂 Xizmat kategoriyasini tanlang:</b>\n\nBarcha narxlar loyiha murakkabligiga qarab muhokama qilinadi.',
        'btn_bots': '🤖 Telegram Botlar',
        'btn_websites': '🌐 Veb-saytlar',
        'btn_security': '🛡️ Xavfsizlik',
        'btn_back': '🔙 Orqaga',
        'btn_order': '✅ Buyurtma',
        
        'service_bots': (
            '<b>🤖 Telegram Bot Ishlab Chiqish</b>\n\n'
            '💰 <b>Narx:</b> 200 TJS / 1800 RUB dan\n'
            '<i>Narx murakkablik va funksionallarga bog\'liq</i>\n\n'
            '✨ <b>Kiritilgan:</b>\n'
            '  • Noldan ishlab chiqish yoki yaxshilash\n'
            '  • Ma\'lumotlar bazasi integratsiyasi\n'
            '  • Admin paneli\n'
            '  • Texnik qo\'llab-quvvatlash\n\n'
            '📋 <b>Rasmiy shartnoma taqdim etiladi</b>\n'
            '⏱ Muddat: 5 ish kunidan'
        ),
        
        'service_websites': (
            '<b>🌐 Veb-sayt Ishlab Chiqish</b>\n\n'
            '💼 <b>Landing sahifalari va korporativ saytlar</b>\n'
            '<i>Narx individual muhokama qilinadi</i>\n\n'
            '✨ <b>Kiritilgan:</b>\n'
            '  • Zamonaviy moslashuvchan dizayn\n'
            '  • SEO optimizatsiyasi\n'
            '  • CRM integratsiyasi\n'
            '  • Kontent boshqaruv tizimi\n\n'
            '📋 <b>Rasmiy shartnoma taqdim etiladi</b>\n'
            '⏱ Muddat: 10 ish kunidan'
        ),
        
        'service_security': (
            '<b>🛡️ Axborot Xavfsizligi</b>\n\n'
            '🔒 <b>Asosiy audit va himoya</b>\n'
            '<i>Narx har bir loyiha uchun individual muhokama qilinadi</i>\n\n'
            '✨ <b>Kiritilgan:</b>\n'
            '  • Dastur xavfsizligi auditi\n'
            '  • Zaifliklar baholash (pentest)\n'
            '  • Xavfsizlik tavsiyalari\n'
            '  • Monitoring tizimini sozlash\n\n'
            '📋 <b>Rasmiy shartnoma taqdim etiladi</b>\n'
            '<i>Biz yuqori narxlar bilan qo\'rqitmaymiz — hamma narsa individual muhokama qilinadi</i>'
        ),
        
        'service_package': (
            '<b>📦 "Tez Boshlash" to\'plami</b>\n\n'
            'Kiradi: Vizitka sayti + Telegram bot + Kanal dizayni.\n\n'
            '💰 <b>Narx:</b> 700 TJS dan'
        ),
        
        'service_ai': (
            '<b>🤖 AI Avtomatlash</b>\n\n'
            'Mahsulotingiz haqida hamma narsani biladigan va mijozlarga 24/7 javob beradigan aqlli yordamchi.\n\n'
            '💰 <b>Narx:</b> 400 TJS dan'
        ),
        
        'service_tech': (
            '<b>🛡️ Texnik Qo\'llab-quvvatlash</b>\n\n'
            '24/7 monitoring, bot yangilanishlari, hujumlar va nosozliklardan himoya.\n\n'
            '💰 <b>Narx:</b> 150 TJS / oy'
        ),
        
        'profile_text': (
            '👤 <b>Sizning profilingiz</b>\n\n'
            '<b>Ism:</b> {name}\n'
            '<b>Foydalanuvchi nomi:</b> {username}\n'
            '<b>ID:</b> <code>{user_id}</code>\n'
            '<b>Til:</b> 🇺🇿 O\'zbekcha\n\n'
            '🌟 Siz Merix CodeX ning qadrli mijozisiz!\n\n'
            '💼 Buyurtma berish uchun <b>«📂 Xizmatlar»</b>ga o\'ting'
        ),
        
        'about_text': (
            'ℹ️ <b>Merix CodeX haqida</b>\n\n'
            '<b>Merix CodeX</b> — professional IT mutaxassislari jamoasi.\n\n'
            '🎯 <b>Bizning missiyamiz:</b>\n'
            'Biznes uchun sifatli texnologik yechimlar taqdim etish.\n\n'
            '💡 <b>Afzalliklar:</b>\n'
            '  • 24/7 Qo\'llab-quvvatlash\n'
            '  • Rasmiy shartnomalar\n'
            '  • Individual yondashuv\n'
            '  • Moslashuvchan narxlar\n\n'
            '� <b>Instagram:</b> https://instagram.com/merix_codex\n\n'
            '�📞 Konsultatsiya uchun <b>«🆘 Yordam»</b>dan foydalaning'
        ),
        
        'help_text': (
            '🆘 <b>24/7 Qo\'llab-quvvatlash</b>\n\n'
            '<b>Qanday buyurtma berish mumkin?</b>\n'
            '1. <b>📂 Xizmatlar</b>ga o\'ting\n'
            '2. Kategoriyani tanlang\n'
            '3. <b>✅ Buyurtma</b>ni bosing\n'
            '4. Vazifangizni tasvirlab bering\n\n'
            '<b>Yordam kerakmi?</b>\n'
            '👨‍💼 Menejerimiz bilan bog\'laning:\n'
            '{admin_link}\n\n'
            '⏰ Biz doim aloqadamiz!'
        ),
        
        'order_description': (
            '📝 <b>Buyurtma: {service}</b>\n\n'
            'Iltimos, vazifangizni batafsil tasvirlab bering:\n\n'
            '• Qanday funksiyalar kerak?\n'
            '• Misollar bormi?\n'
            '• Muddatlar?\n\n'
            'Qanchalik batafsil tavsif = aniqroq baholash.'
        ),
        'order_confirmation': (
            '✅ <b>So\'rovingizni tekshiring</b>\n\n'
            '<b>Xizmat:</b> {service}\n\n'
            '<b>Tavsif:</b>\n{description}\n\n'
            'Agar to\'g\'ri bo\'lsa, <b>«✅ Yuborish»</b>ni bosing.'
        ),
        'btn_send': '✅ Yuborish',
        'btn_cancel': '❌ Bekor qilish',
        'order_sent': (
            '✅ <b>So\'rov muvaffaqiyatli yuborildi!</b>\n\n'
            'Menejerimiz tez orada siz bilan bog\'lanadi.\n\n'
            '⏰ O\'rtacha javob vaqti: 1-2 soat'
        ),
        'order_cancelled': '❌ <b>So\'rov bekor qilindi</b>\n\nIstalgan vaqtda yangi so\'rov yaratishingiz mumkin.',
        'order_error': '❌ <b>So\'rov yuborishda xatolik</b>\n\nKeyinroq urinib ko\'ring yoki to\'g\'ridan-to\'g\'ri <b>🆘 Yordam</b> orqali bog\'laning.',
        
        'admin_new_order': (
            '🔔 <b>Yangi buyurtma!</b>\n\n'
            '<b>Xizmat:</b> {service}\n\n'
            '👤 <b>Mijoz:</b> {name}\n'
            '📱 <b>Foydalanuvchi nomi:</b> {username}\n'
            '🆔 <b>ID:</b> <code>{user_id}</code>\n'
            '🌐 <b>Til:</b> {language}\n\n'
            '<b>Tavsif:</b>\n{description}'
        ),
        
        'admin_panel': '🔐 <b>Admin Paneli</b>\n\nAmalni tanlang:',
        'btn_statistics': '📊 Statistika',
        'btn_broadcast': '📢 E\'lon',
        'statistics_text': '📊 <b>Bot Statistikasi</b>\n\n👥 Jami foydalanuvchilar: <b>{count}</b>',
        'broadcast_prompt': '📢 <b>Xabar tarqatish</b>\n\nBarcha foydalanuvchilarga yubormoqchi bo\'lgan xabaringizni yuboring:',
        'broadcast_success': '✅ <b>Tarqatish yakunlandi</b>\n\n📤 Yuborildi: {success}\n❌ Xatolar: {failed}',
        'not_admin': '❌ Sizda bu buyruqqa ruxsat yo\'q.',
    }
}


# Языковые флаги для кнопок
LANGUAGE_FLAGS = {
    'ru': '🇷🇺',
    'en': '🇺🇸',
    'tj': '🇹🇯',
    'uz': '🇺🇿'
}

# Полные названия языков
LANGUAGE_NAMES = {
    'ru': 'Русский',
    'en': 'English',
    'tj': 'Тоҷикӣ',
    'uz': 'O\'zbekcha'
}


def get_text(lang: str, key: str, **kwargs) -> str:
    """
    Получает переведенный текст для указанного языка
    
    Args:
        lang: Код языка ('ru', 'en', 'tj', 'uz')
        key: Ключ текста из словаря
        **kwargs: Параметры для форматирования текста
        
    Returns:
        str: Переведенный текст
    """
    # Если язык не найден, используем русский по умолчанию
    if lang not in TRANSLATIONS:
        lang = 'ru'
    
    # Получаем текст
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS['ru'].get(key, f'[Missing: {key}]'))
    
    # Форматируем если есть параметры
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text
