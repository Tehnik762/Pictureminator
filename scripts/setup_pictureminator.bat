@echo off
title Pictureminator - Setup Environment
color 0A
cls
echo ========================================
echo     Pictureminator - Setup Script
echo ========================================
echo.

:: === Step 1. Check for Python ===
echo [INFO] Checking for Python...
set "PYTHON_PATH=python"

python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [W] Python not found in PATH.
    if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
        set "PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
        echo [OK] Found Python manually at "%PYTHON_PATH%"
    ) else (
        echo [Q] Python 3.10 not detected. Install now? (Y/N)
        set /p choice="> "
        if /I "%choice%"=="Y" (
            call "%~dp0install_python.bat"
            echo [INFO] Rechecking after install...
            timeout /t 3 >nul
            if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe" (
                set "PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe"
            ) else (
                echo [E] Python installation failed or PATH not updated.
                echo Restart Windows and rerun setup.
                pause
                exit /b
            )
        ) else (
            echo [E] Python required. Exiting setup.
            pause
            exit /b
        )
    )
)

for /f "delims=" %%i in ('"%PYTHON_PATH%" --version 2^>^&1') do set PYVER=%%i
echo [OK] Using %PYVER% at "%PYTHON_PATH%"
echo.

:: === Step 2. Virtual environment ===
if exist ".venv\Scripts\activate.bat" (
    echo [i] Virtual environment already exists.
    echo [Q] Recreate it? Y/N
    set /p recreate="> "
    if /I "%recreate%"=="Y" (
        rmdir /s /q .venv
        echo [INFO] Recreating virtual environment...
        "%PYTHON_PATH%" -m venv .venv
    ) else (
        echo [SKIP] Using existing virtual environment.
    )
) else (
    echo [INFO] Creating new virtual environment...
    "%PYTHON_PATH%" -m venv .venv
)
echo.

:: === Step 3. Activate & install dependencies ===
echo [INFO] Activating environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [E] Failed to activate virtual environment.
    pause
    exit /b
)

echo [INFO] Installing dependencies...
python -m pip install --upgrade pip
if exist "requirements.txt" (
    python -m pip install -r requirements.txt
) else (
    echo [W] requirements.txt not found — skipping dependency install.
)
echo.
echo [OK] Environment setup complete.
pause
