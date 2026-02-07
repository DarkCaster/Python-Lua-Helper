@echo off
setlocal

set "script_dir=%~dp0"
set "venv_dir=%script_dir%venv"

if not exist "%venv_dir%" (
    echo No venv directory found, run init.bat to initialize it...
    pause
    exit /b 1
)

echo Activating venv
call "%venv_dir%\Scripts\activate.bat"

"%venv_dir%\Scripts\python" %*

endlocal
