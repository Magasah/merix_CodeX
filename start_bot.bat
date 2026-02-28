@echo off
echo ============================================
echo   Запуск Telegram бота Merix CodeX
echo ============================================
echo.

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
	echo [0/3] Создание виртуального окружения...
	py -3 -m venv .venv
)

echo [1/3] Проверка зависимостей...
".venv\Scripts\python.exe" -m pip install -r requirements.txt >nul 2>&1

echo [2/3] Запуск бота...
echo.
echo Бот запускается...
echo Для остановки нажмите Ctrl+C
echo.
echo ============================================
echo.

".venv\Scripts\python.exe" main.py

pause
