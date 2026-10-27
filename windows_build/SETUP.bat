@echo off
chcp 65001 >nul
echo PNEVMA Symbiosis Unified — Windows
echo [1] Run demo
echo [2] Portable install to %%LOCALAPPDATA%%
echo [3] Exit
set /p c="Choice: "
if "%c%"=="1" (
  cd /d "%~dp0.."
  python run.py --demo
  pause
)
if "%c%"=="2" (
  powershell -ExecutionPolicy Bypass -File "%~dp0installer\Install-Portable.ps1"
  pause
)
