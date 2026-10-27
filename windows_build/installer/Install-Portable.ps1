$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$InstallDir = Join-Path $env:LOCALAPPDATA "PnevmaSymbiosisUnified"
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Copy-Item -Recurse -Force (Join-Path $Root "src") $InstallDir
Copy-Item -Force (Join-Path $Root "run.py") $InstallDir
Copy-Item -Force (Join-Path $Root "README.md") $InstallDir
$start = @"
@echo off
cd /d "%~dp0"
python run.py --demo
pause
"@
Set-Content (Join-Path $InstallDir "START.bat") $start
$W = New-Object -ComObject WScript.Shell
$sc = $W.CreateShortcut((Join-Path ([Environment]::GetFolderPath("Desktop")) "PNEVMA Symbiosis.lnk"))
$sc.TargetPath = Join-Path $InstallDir "START.bat"
$sc.WorkingDirectory = $InstallDir
$sc.Save()
Write-Host "Installed to $InstallDir"
