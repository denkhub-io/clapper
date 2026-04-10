@echo off
:: Avvia clapper su Windows — se manca il venv, lancia l'installer
set SCRIPT_DIR=%~dp0

if not exist "%SCRIPT_DIR%.venv" (
    call "%SCRIPT_DIR%install.bat"
)

"%SCRIPT_DIR%.venv\Scripts\python.exe" "%SCRIPT_DIR%clapper.py" %*
