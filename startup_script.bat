@echo off
title Personal Automation Hub Startup
echo.
echo ========================================
echo    🚀 PERSONAL AUTOMATION HUB 🚀
echo    Starting Automatically on Boot
echo ========================================
echo.

REM Change to the project directory
cd /d "D:\python\Agents"

REM Wait a bit for system to fully boot
timeout /t 30 /nobreak >nul

echo Starting automation system...
echo.

REM Start the system tray application (runs in background)
start /min pythonw system_tray_app.py

REM Wait a moment for the app to start
timeout /t 10 /nobreak >nul

echo.
echo ✅ Automation Hub started successfully!
echo 📱 Look for the blue icon in your system tray
echo 🖱️ Right-click for menu options
echo.
echo This window will close automatically in 10 seconds...
timeout /t 10 /nobreak >nul

exit
