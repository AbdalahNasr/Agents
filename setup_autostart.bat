@echo off
title Setup Auto-Start for Personal Automation Hub
echo.
echo ========================================
echo    🚀 SETUP AUTO-START SYSTEM 🚀
echo    This will make your automation run automatically on boot
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running as Administrator
) else (
    echo ❌ This script must run as Administrator
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo.
echo Setting up automatic startup...
echo.

REM Create the startup task
schtasks /create /tn "PersonalAutomationHub" /tr "D:\python\Agents\startup_script.bat" /sc onstart /ru "SYSTEM" /f

if %errorLevel% == 0 (
    echo ✅ Task created successfully!
    echo.
    echo Your automation system will now start automatically when Windows boots.
    echo.
    echo To test it now, you can:
    echo 1. Restart your computer, OR
    echo 2. Run the task manually: schtasks /run /tn "PersonalAutomationHub"
    echo.
    echo To remove the auto-start later:
    echo schtasks /delete /tn "PersonalAutomationHub" /f
) else (
    echo ❌ Failed to create task
    echo Error code: %errorLevel%
)

echo.
echo Setup complete!
pause
