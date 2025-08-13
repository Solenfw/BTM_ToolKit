@echo off

REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Build the executable
pyinstaller --name BTM_Quote_Tool ^
            --onefile ^
            --windowed ^
            --add-data "data;data" ^
            --add-data "src/config.json;." ^
            src/main.py

REM Deactivate the virtual environment
deactivate
