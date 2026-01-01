@echo off
title Install - YouTube Bot
color 0B

cd /d "%~dp0"

echo.
echo ================================================
echo    YOUTUBE BOT - INSTALL
echo ================================================
echo.
echo Folder: %cd%
echo.
echo Installing aiogram...
echo Please wait...
echo.

pip install aiogram

echo.
echo ================================================
if %errorlevel% equ 0 (
    echo    SUCCESS!
    echo.
    echo    Now run start.bat
) else (
    echo    ERROR!
    echo.
    echo    Check if Python is installed:
    echo    python --version
)
echo ================================================
echo.
pause
