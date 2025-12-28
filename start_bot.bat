@echo off
echo ============================================
echo   Запуск Telegram бота Merix CodeX
echo ============================================
echo.

cd /d "%~dp0"

echo [1/3] Проверка зависимостей...
pip install -r requirements.txt >nul 2>&1

echo [2/3] Запуск бота...
echo.
echo Бот запускается...
echo Для остановки нажмите Ctrl+C
echo.
echo ============================================
echo.

python main.py

pause
