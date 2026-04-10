@echo off
:: Clapper — install e setup su Windows

echo.
echo   ┌─────────────────────────────────┐
echo   │   CLAPPER INSTALLER             │
echo   └─────────────────────────────────┘
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo   X Python non trovato. Installalo da python.org e riprova.
    exit /b 1
)
echo   V Python trovato

set SCRIPT_DIR=%~dp0
set VENV_DIR=%SCRIPT_DIR%.venv

if not exist "%VENV_DIR%" (
    echo   - Creo ambiente virtuale...
    python -m venv "%VENV_DIR%"
)
echo   V Ambiente virtuale pronto

echo   - Installo dipendenze...
"%VENV_DIR%\Scripts\pip.exe" install --quiet sounddevice numpy pyttsx3
echo   V Dipendenze installate

echo.
"%VENV_DIR%\Scripts\python.exe" "%SCRIPT_DIR%clapper.py" setup
