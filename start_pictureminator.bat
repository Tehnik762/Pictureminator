@echo off
title Pictureminator - Start GUI
cd /d "%~dp0"
echo.
echo ================================
echo   Starting Pictureminator GUI
echo ================================
echo.

:: 1. Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo [E] Virtual environment not found.
    echo Run setup_pictureminator.bat first.
    pause
    exit /b 1
)

:: 2. Activate the environment
call ".venv\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo [E] Failed to activate .venv.
    pause
    exit /b 1
)

:: 3. Set Qt5 bin path (for DLLs)
set "QT_BIN=%CD%\.venv\Lib\site-packages\PyQt5\Qt5\bin"
if exist "%QT_BIN%" (
    set "PATH=%QT_BIN%;%PATH%"
) else (
    echo [W] Qt5 bin not found — PyQt5 might not load.
)

:: 4. Run the GUI (interface or main)
if exist "interface\Pictureminator_GUI.py" (
    echo [i] Launching interface\Pictureminator_GUI.py ...
    python "interface\Pictureminator_GUI.py"
) else if exist "pictureminator.py" (
    echo [i] Launching pictureminator.py ...
    python "pictureminator.py"
) else (
    echo [E] Could not find Pictureminator GUI file.
    pause
    exit /b 1
)

echo.
echo [OK] Application finished.
echo.
pause
