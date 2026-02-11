@echo off
title Pictureminator - Start
color 0A
setlocal
cd /d "%~dp0"

echo [START] %DATE% %TIME%

:: === Detect root folder ===
cd ..
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] .venv missing in project root.
    echo Run setup_pictureminator.bat first.
    pause
    exit /b 1
)

:: === Activate virtual environment ===
call .venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to activate .venv.
    pause
    exit /b 2
)

:: === Add Qt5 bin path to PATH (for DLLs) ===
set "QT_BIN=%CD%\.venv\Lib\site-packages\PyQt5\Qt5\bin"
if exist "%QT_BIN%" (
    echo [INFO] Adding Qt bin to PATH...
    set "PATH=%QT_BIN%;%PATH%"
) else (
    echo [WARN] Qt bin not found. PyQt5 DLL errors possible.
)

:: === Run Pictureminator ===
if exist "interface\Pictureminator_GUI.py" (
    echo [INFO] Launching interface\Pictureminator_GUI.py...
    python "interface\Pictureminator_GUI.py"
) else if exist "pictureminator.py" (
    echo [INFO] Launching pictureminator.py...
    python "pictureminator.py"
) else (
    echo [ERROR] GUI file not found.
    pause
    exit /b 3
)

echo.
echo [OK] Application finished.
pause
exit /b 0
