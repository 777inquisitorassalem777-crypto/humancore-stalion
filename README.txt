PNEVMA Symbiosis — Portable Installer
=====================================
No Inno Setup. No admin rights. No Setup.exe required.

INSTALL (recommended)
  Double-click:  INSTALL.bat
  or:
  powershell -ExecutionPolicy Bypass -File INSTALL.ps1

  Installs to:  %LOCALAPPDATA%\PnevmaSymbiosis
  Creates:      Desktop + Start Menu shortcuts
  Uninstall:    run UNINSTALL.bat inside install folder

RUN WITHOUT INSTALL
  Double-click:  RUN_WITHOUT_INSTALL.bat

REQUIREMENT
  Python 3.10+ with "Add to PATH"
  https://www.python.org/downloads/

OPTIONAL: build standalone EXE later
  Use PNEVMA_Symbiosis_Windows_EXE_Builder.zip + BUILD_EXE.bat
  Then you can replace run.py flow with the .exe in START.bat
