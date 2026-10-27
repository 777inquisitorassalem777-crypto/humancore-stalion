@echo off
chcp 65001 >nul
cd /d "%~dp0app"
where python >nul 2>&1
if errorlevel 1 (
  echo Python not found. Install from https://www.python.org
  pause
  exit /b 1
)
python run.py --demo
pause
