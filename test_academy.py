"""
Тестовый скрипт для проверки Merix Academy функционала
Запустите этот скрипт для проверки всех компонентов
"""
import sys
import os

def check_imports():
    """Проверка всех импортов"""
    print("🔍 Проверка импортов...")
    
    try:
        import config
        print("✅ config.py импортирован")
        
        # Проверка констант
        assert hasattr(config, 'PRIVATE_CHANNEL_ID'), "❌ PRIVATE_CHANNEL_ID не найден"
        assert hasattr(config, 'PAYMENT_CARD_ALIF'), "❌ PAYMENT_CARD_ALIF не найден"
        assert hasattr(config, 'PAYMENT_CARD_MASTERCARD'), "❌ PAYMENT_CARD_MASTERCARD не найден"
        print(f"  ✓ PRIVATE_CHANNEL_ID: {config.PRIVATE_CHANNEL_ID}")
        print(f"  ✓ PAYMENT_CARD_ALIF: {config.PAYMENT_CARD_ALIF}")
        print(f"  ✓ PAYMENT_CARD_MASTERCARD: {config.PAYMENT_CARD_MASTERCARD}")
        
    except Exception as e:
        print(f"❌ Ошибка config.py: {e}")
        return False
    
    try:
        from states.order import SubscriptionStates
        print("✅ SubscriptionStates импортирован")
        assert hasattr(SubscriptionStates, 'waiting_for_receipt'), "❌ waiting_for_receipt не найден"
        print("  ✓ waiting_for_receipt состояние добавлено")
    except Exception as e:
        print(f"❌ Ошибка states/order.py: {e}")
        return False
    
    try:
        from keyboards.inline import (
            get_subscription_plans_keyboard,
            get_payment_approval_keyboard,
            get_services_keyboard
        )
        print("✅ Клавиатуры импортированы")
        
        # Тестовая генерация клавиатур
        kb1 = get_subscription_plans_keyboard()
        kb2 = get_payment_approval_keyboard(123456)
        kb3 = get_services_keyboard('ru')
        
        print("  ✓ get_subscription_plans_keyboard() работает")
        print("  ✓ get_payment_approval_keyboard() работает")
        print("  ✓ get_services_keyboard() содержит Merix Academy")
        
        # Проверяем наличие кнопки Merix Academy
        has_academy = False
        for row in kb3.inline_keyboard:
            for button in row:
                if "Merix Academy" in button.text:
                    has_academy = True
                    break
        
        if has_academy:
            print("  ✓ Кнопка 'Merix Academy' найдена в Services")
        else:
            print("  ⚠️ Кнопка 'Merix Academy' НЕ найдена в Services")
            
    except Exception as e:
        print(f"❌ Ошибка keyboards/inline.py: {e}")
        return False
    
    try:
        from handlers import merix_academy
        print("✅ handlers/merix_academy.py импортирован")
        
        # Проверка наличия основных функций
        functions = [
            'show_merix_academy',
            'process_subscription_payment',
            'pre_checkout_handler',
            'successful_payment_handler',
            'show_manual_payment',
            'receive_payment_receipt',
            'approve_manual_payment',
            'reject_manual_payment'
        ]
        
        for func_name in functions:
            assert hasattr(merix_academy, func_name), f"❌ Функция {func_name} не найдена"
        
        print(f"  ✓ Все {len(functions)} функций присутствуют")
        
        # Проверка констант
        assert hasattr(merix_academy, 'SUBSCRIPTION_PLANS'), "❌ SUBSCRIPTION_PLANS не найден"
        plans = merix_academy.SUBSCRIPTION_PLANS
        assert len(plans) == 3, f"❌ Ожидается 3 тарифа, найдено {len(plans)}"
        print(f"  ✓ Найдено {len(plans)} тарифных плана")
        
        # Проверка роутера
        assert hasattr(merix_academy, 'router'), "❌ Router не найден"
        print("  ✓ Router зарегистрирован")
        
    except Exception as e:
        print(f"❌ Ошибка handlers/merix_academy.py: {e}")
        return False
    
    try:
        from handlers import routers
        print("✅ handlers/__init__.py импортирован")
        
        # Проверяем количество роутеров
        print(f"  ✓ Зарегистрировано роутеров: {len(routers)}")
        
        # Проверяем наличие academy_router
        from handlers.merix_academy import router as academy_router
        if academy_router in routers:
            print("  ✓ academy_router зарегистрирован в списке роутеров")
        else:
            print("  ⚠️ academy_router НЕ найден в списке роутеров")
            
    except Exception as e:
        print(f"❌ Ошибка handlers/__init__.py: {e}")
        return False
    
    return True


def check_file_structure():
    """Проверка структуры файлов"""
    print("\n📁 Проверка файловой структуры...")
    
    required_files = {
        'handlers/merix_academy.py': 'Основной обработчик',
        'MERIX_ACADEMY_README.md': 'Подробная документация',
        'QUICK_START_ACADEMY.md': 'Быстрый старт',
        'SUMMARY_CHANGES.md': 'Итоговая сводка'
    }
    
    all_exist = True
    for filepath, description in required_files.items():
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {filepath} ({size} bytes) - {description}")
        else:
            print(f"❌ {filepath} НЕ НАЙДЕН - {description}")
            all_exist = False
    
    return all_exist


def check_constants():
    """Проверка важных констант"""
    print("\n⚙️ Проверка конфигурации...")
    
    import config
    
    checks = [
        ('PRIVATE_CHANNEL_ID', config.PRIVATE_CHANNEL_ID, int, -1003543534808),
        ('PAYMENT_CARD_ALIF', config.PAYMENT_CARD_ALIF, str, "+992888788181"),
        ('PAYMENT_CARD_MASTERCARD', config.PAYMENT_CARD_MASTERCARD, str, "5413525250170749"),
    ]
    
    all_ok = True
    for name, value, expected_type, expected_value in checks:
        if isinstance(value, expected_type):
            if value == expected_value:
                print(f"✅ {name} = {value} (корректно)")
            else:
                print(f"⚠️ {name} = {value} (ожидалось: {expected_value})")
        else:
            print(f"❌ {name} имеет неверный тип: {type(value)} (ожидался: {expected_type})")
            all_ok = False
    
    return all_ok


def check_callback_handlers():
    """Проверка обработчиков callback"""
    print("\n🔧 Проверка callback обработчиков...")
    
    try:
        from handlers.merix_academy import router
        from aiogram import Router
        
        # Подсчитываем обработчики
        callback_count = 0
        message_count = 0
        pre_checkout_count = 0
        
        for observer in router.observers.values():
            for handler in observer:
                if 'callback_query' in str(handler):
                    callback_count += 1
                elif 'message' in str(handler):
                    message_count += 1
                elif 'pre_checkout_query' in str(handler):
                    pre_checkout_count += 1
        
        print(f"✅ Callback обработчиков: {callback_count}")
        print(f"✅ Message обработчиков: {message_count}")
        print(f"✅ Pre-checkout обработчиков: {pre_checkout_count}")
        
        expected_callbacks = [
            'merix_academy',
            'sub_7_days', 'sub_14_days', 'sub_30_days',
            'pay_manual',
            'approve_pay_', 'reject_pay_'
        ]
        
        print(f"\n  Ожидаемые callback_data:")
        for cb in expected_callbacks:
            print(f"    • {cb}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при проверке обработчиков: {e}")
        return False


def main():
    """Основная функция тестирования"""
    print("="*60)
    print("🧪 ТЕСТИРОВАНИЕ MERIX ACADEMY ИНТЕГРАЦИИ")
    print("="*60)
    
    results = []
    
    # Тест 1: Импорты
    results.append(("Импорты модулей", check_imports()))
    
    # Тест 2: Структура файлов
    results.append(("Файловая структура", check_file_structure()))
    
    # Тест 3: Константы
    results.append(("Конфигурация", check_constants()))
    
    # Тест 4: Обработчики
    results.append(("Callback обработчики", check_callback_handlers()))
    
    # Итоговый отчет
    print("\n" + "="*60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Система готова к использованию!")
        print("\n💡 Следующий шаг: python main.py")
    else:
        print("⚠️ ЕСТЬ ПРОБЛЕМЫ! Проверьте ошибки выше.")
        print("\n💡 Проверьте файлы и повторите тестирование.")
    
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
