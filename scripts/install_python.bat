@echo off
title Install Python 3.10
color 0A
cd /d "%~dp0"

echo.
echo =========================================
echo     Pictureminator - Python Installer
echo =========================================
echo.

set "PYTHON_INSTALLER=%TEMP%\python-3.10.11-amd64.exe"
set "PYTHON_URL=https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"

echo [INFO] Downloading Python 3.10.11 (64-bit)...
powershell -Command "try { Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%' -UseBasicParsing } catch { exit 1 }"
if not exist "%PYTHON_INSTALLER%" (
    echo [ERROR] Download failed. Check internet connection.
    pause
    exit /b 1
)

echo [INFO] Installing Python globally (silent mode)...
start /wait "" "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_doc=0 Include_launcher=0

if exist "%PYTHON_INSTALLER%" del "%PYTHON_INSTALLER%" >nul 2>&1

echo [INFO] Adding Python 3.10 to system PATH...
setx /M PATH "%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\"

echo.
echo [CHECK] Verifying installation...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python installed but PATH not yet active.
    echo [i] Please RESTART Windows, then reopen Pictureminator Manager.
    pause
    exit /b 0
) else (
