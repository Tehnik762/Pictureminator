@echo off
title Pictureminator Manager
color 0A
setlocal enabledelayedexpansion

:: Set folder path for scripts (în caz că rulezi din alt loc)
set "SCRIPT_DIR=%~dp0scripts"

:menu
cls
echo ========================================
echo        Pictureminator - Manager
echo ========================================
echo.
echo  [1] Start Pictureminator
echo  [2] Setup (Install Python + Virtual Environment)
echo  [3] Reinstall Python 3.10
echo  [4] Open Scripts Folder
echo  [5] Exit
echo.
set /p choice="Select an option: "

if "%choice%"=="1" (
    if exist "%SCRIPT_DIR%\start_pictureminator.bat" (
        call "%SCRIPT_DIR%\start_pictureminator.bat"
    ) else (
        echo [E] start_pictureminator.bat not found in scripts folder.
        pause
    )
    goto menu
)

if "%choice%"=="2" (
    if exist "%SCRIPT_DIR%\setup_pictureminator.bat" (
        call "%SCRIPT_DIR%\setup_pictureminator.bat"
    ) else (
        echo [E] setup_pictureminator.bat not found in scripts folder.
        pause
    )
    goto menu
)

if "%choice%"=="3" (
    if exist "%SCRIPT_DIR%\install_python.bat" (
        call "%SCRIPT_DIR%\install_python.bat"
    ) else (
        echo [E] install_python.bat not found in scripts folder.
        pause
    )
    goto menu
)

if "%choice%"=="4" (
    echo [INFO] Opening scripts folder...
    explorer "%SCRIPT_DIR%"
    goto menu
)

if "%choice%"=="5" exit

echo [W] Invalid selection. Try again.
timeout /t 2 >nul
goto menu
