# PNEVMA Symbiosis — Portable Installer (PowerShell)
$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$Src = Join-Path $Root "app"
$InstallDir = Join-Path $env:LOCALAPPDATA "PnevmaSymbiosis"

Write-Host "============================================"
Write-Host " PNEVMA Symbiosis Unified v1.0"
Write-Host " Portable Installer"
Write-Host " Target: $InstallDir"
Write-Host "============================================"

New-Item -ItemType Directory -Force -Path (Join-Path $InstallDir "src\pnevma_symbiosis") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $InstallDir "tests") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $InstallDir "data") | Out-Null

Copy-Item -Force (Join-Path $Src "src\pnevma_symbiosis\*") (Join-Path $InstallDir "src\pnevma_symbiosis\")
Copy-Item -Force (Join-Path $Src "run.py") $InstallDir
Copy-Item -Force (Join-Path $Src "README.md") $InstallDir
if (Test-Path (Join-Path $Src "tests\test_symbiosis.py")) {
  Copy-Item -Force (Join-Path $Src "tests\test_symbiosis.py") (Join-Path $InstallDir "tests\")
}

@"
@echo off
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>&1
if errorlevel 1 (
  echo Python not found. Install from https://www.python.org
  pause
  exit /b 1
)
python run.py --demo
pause
"@ | Set-Content -Path (Join-Path $InstallDir "START.bat") -Encoding ASCII

@"
@echo off
chcp 65001 >nul
cd /d "%~dp0"
python run.py --status
pause
"@ | Set-Content -Path (Join-Path $InstallDir "START_STATUS.bat") -Encoding ASCII

@"
@echo off
chcp 65001 >nul
echo Removing portable install...
rmdir /s /q "%LOCALAPPDATA%\PnevmaSymbiosis" 2>nul
del "%USERPROFILE%\Desktop\PNEVMA Symbiosis.lnk" 2>nul
echo Done.
pause
"@ | Set-Content -Path (Join-Path $InstallDir "UNINSTALL.bat") -Encoding ASCII

$W = New-Object -ComObject WScript.Shell
$desk = [Environment]::GetFolderPath("Desktop")
$sc = $W.CreateShortcut((Join-Path $desk "PNEVMA Symbiosis.lnk"))
$sc.TargetPath = Join-Path $InstallDir "START.bat"
$sc.WorkingDirectory = $InstallDir
$sc.Description = "PNEVMA Symbiosis Unified"
$sc.Save()

$sm = Join-Path ([Environment]::GetFolderPath("StartMenu")) "Programs\PNEVMA Symbiosis"
New-Item -ItemType Directory -Force -Path $sm | Out-Null
$sc2 = $W.CreateShortcut((Join-Path $sm "PNEVMA Symbiosis.lnk"))
$sc2.TargetPath = Join-Path $InstallDir "START.bat"
$sc2.WorkingDirectory = $InstallDir
$sc2.Save()

Write-Host ""
Write-Host "INSTALLED -> $InstallDir"
Write-Host "Desktop shortcut created. Run START.bat or the shortcut."
Write-Host "Requires Python 3.10+ in PATH."
