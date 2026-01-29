@echo off
REM Installer Builder Frontend GUI launcher

echo Starting Installer Builder Frontend...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Run the GUI application
python "%~dp0installerbuildergui.py"

if errorlevel 1 (
    echo.
    echo An error occurred. Check the output above.
    pause
)

