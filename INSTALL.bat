@echo off
chcp 65001 >nul
title PNEVMA Symbiosis — Portable Installer
cd /d "%~dp0"

echo ============================================
echo  PNEVMA Symbiosis Unified v1.0
echo  Portable Installer (no admin, no Inno)
echo ============================================
echo.

set "INSTALL_DIR=%LOCALAPPDATA%\PnevmaSymbiosis"
set "SRC=%~dp0app"

echo Install to:
echo   %INSTALL_DIR%
echo.
set /p CONFIRM="Continue? [Y/N]: "
if /i not "%CONFIRM%"=="Y" if /i not "%CONFIRM%"=="Yes" (
  echo Cancelled.
  pause
  exit /b 0
)

echo.
echo [1/4] Creating folders...
mkdir "%INSTALL_DIR%" 2>nul
mkdir "%INSTALL_DIR%\src\pnevma_symbiosis" 2>nul
mkdir "%INSTALL_DIR%\tests" 2>nul
mkdir "%INSTALL_DIR%\data" 2>nul

echo [2/4] Copying files...
xcopy /E /I /Y "%SRC%\src\pnevma_symbiosis\*" "%INSTALL_DIR%\src\pnevma_symbiosis\" >nul
copy /Y "%SRC%\run.py" "%INSTALL_DIR\" >nul
copy /Y "%SRC%\README.md" "%INSTALL_DIR\" >nul
if exist "%SRC%\tests\test_symbiosis.py" copy /Y "%SRC%\tests\test_symbiosis.py" "%INSTALL_DIR%\tests\" >nul

echo [3/4] Writing launchers...

REM START.bat
(
echo @echo off
echo chcp 65001 ^>nul
echo cd /d "%%~dp0"
echo where python ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo   echo Python not found. Install from https://www.python.org
echo   pause
echo   exit /b 1
echo ^)
echo python run.py --demo
echo pause
) > "%INSTALL_DIR%\START.bat"

REM START_STATUS.bat
(
echo @echo off
echo chcp 65001 ^>nul
echo cd /d "%%~dp0"
echo python run.py --status
echo pause
) > "%INSTALL_DIR%\START_STATUS.bat"

REM UNINSTALL.bat
(
echo @echo off
echo chcp 65001 ^>nul
echo echo Removing PNEVMA Symbiosis portable install...
echo set "D=%%LOCALAPPDATA%%\PnevmaSymbiosis"
echo rmdir /s /q "%%D%%" 2^>nul
echo del "%%USERPROFILE%%\Desktop\PNEVMA Symbiosis.lnk" 2^>nul
echo echo Done.
echo pause
) > "%INSTALL_DIR%\UNINSTALL.bat"

echo [4/4] Desktop shortcut...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$W=New-Object -ComObject WScript.Shell; $s=$W.CreateShortcut([Environment]::GetFolderPath('Desktop')+'\PNEVMA Symbiosis.lnk'); $s.TargetPath='%INSTALL_DIR%\START.bat'; $s.WorkingDirectory='%INSTALL_DIR%'; $s.Description='PNEVMA Symbiosis Unified'; $s.Save()"

REM Start Menu
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$sm=[Environment]::GetFolderPath('StartMenu')+'\Programs\PNEVMA Symbiosis'; New-Item -ItemType Directory -Force -Path $sm | Out-Null; $W=New-Object -ComObject WScript.Shell; $s=$W.CreateShortcut($sm+'\PNEVMA Symbiosis.lnk'); $s.TargetPath='%INSTALL_DIR%\START.bat'; $s.WorkingDirectory='%INSTALL_DIR%'; $s.Save()"

echo.
echo ============================================
echo  INSTALLED
echo  Folder:  %INSTALL_DIR%
echo  Desktop shortcut: PNEVMA Symbiosis
echo  Run: START.bat  or  desktop icon
echo  Needs: Python 3.10+ in PATH
echo ============================================
pause
