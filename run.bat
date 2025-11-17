@echo off
setlocal

set "script_dir=%~dp0"
set "venv_dir=%script_dir%venv"

if not exist "%venv_dir%" (
    python3 -m venv "%venv_dir%"
    "%venv_dir%\Scripts\python3" -m pip --require-virtualenv install --upgrade pip build
)

"%venv_dir%\Scripts\python3" %*

endlocal
