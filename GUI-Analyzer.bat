@echo off

if exist "venv" (
    set "venv_path=venv"
    goto activate_venv
) else if exist "env" (
    set "venv_path=env"
    goto activate_venv
)

echo No virtual environment found. Creating a new one...
python -m venv venv
set "venv_path=venv"
echo The virtual environment is created in the “venv” dir.
call "%venv_path%\Scripts\activate.bat"
echo Uploading requirements...
if exist "requirements.txt" pip install -r requirements.txt >nul 2>&1

:activate_venv
python main.py
exit