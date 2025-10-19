@echo off
cd /d "%~dp0"
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install lazy_loader --upgrade
python -m pip install --force-reinstall PyQt5==5.15.10 PyQt5-Qt5==5.15.2 PyQt5-sip==12.13.0
pause
