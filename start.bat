@echo off
title YouTube Bot
color 0A

cd /d "%~dp0"

echo.
echo ================================================
echo    YOUTUBE VERIFICATION BOT
echo    Starting...
echo ================================================
echo.
echo Folder: %cd%
echo.

if not exist "bot.py" (
    echo.
    echo ================================================
    echo    ERROR: bot.py not found
    echo ================================================
    echo.
    pause
    exit /b 1
)

python bot.py

if %errorlevel% neq 0 (
    echo.
    echo ================================================
    echo    ERROR
    echo ================================================
    echo.
    pause
)
