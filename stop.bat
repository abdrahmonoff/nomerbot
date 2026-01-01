@echo off
title Stop Bot
color 0C

echo.
echo ================================================
echo    Stopping bot...
echo ================================================
echo.

taskkill /F /IM python.exe /T 2>nul
taskkill /F /IM pythonw.exe /T 2>nul

if %errorlevel% equ 0 (
    echo Bot stopped successfully!
) else (
    echo Bot was not running.
)

echo.
pause
