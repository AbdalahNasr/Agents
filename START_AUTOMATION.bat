@echo off
echo Starting Continuous Job Application Automation...
echo.
echo This will run 24/7 until you stop it.
echo Press Ctrl+C to stop the automation.
echo.
cd /d "D:\python\Agents"
python continuous_job_automation.py
pause