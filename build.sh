#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build the executable
pyinstaller --name BTM_Quote_Tool \
            --onefile \
            --windowed \
            --add-data "data:data" \
            --add-data "src/config.json:." \
            src/main.py

# Deactivate the virtual environment
deactivate
