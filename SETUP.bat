@echo off
chcp 65001 >nul
title PNEVMA Symbiosis Unified Setup
echo ============================================
echo  PNEVMA Symbiosis Unified v1.0
echo ============================================
echo  [1] Run demo
echo  [2] Portable install
echo  [3] Build EXE (PyInstaller + Python required)
echo  [4] Exit
set /p c="Select: "
if "%c%"=="1" (cd /d "%~dp0" & python run.py --demo & pause & exit /b 0)
if "%c%"=="2" (powershell -ExecutionPolicy Bypass -File "%~dp0windows_build\installer\Install-Portable.ps1" & pause & exit /b 0)
if "%c%"=="3" (
  python -m pip install pyinstaller -q
  python -m PyInstaller --noconfirm --onefile --name PnevmaSymbiosis --paths src run.py
  echo EXE: dist\PnevmaSymbiosis.exe
  pause
  exit /b 0
)
