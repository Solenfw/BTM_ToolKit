import json
import logging
from logging import Logger
import os
from pathlib import Path
import csv
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from .string_utilities import string_cleaner

def load_config(config_file=""):
    """Loads PATH configuration from a JSON file."""
    # If no config file is specified, look for a .json file in the current directory
    if not config_file:
        json_files = [file for file in os.listdir('.') if file.endswith('.json')]
        if not json_files:
            print("No JSON configuration file found.")
            return None
        # Automatically select the first .json file found
        config_file = json_files[0]
        print(f"No file specified. Using {config_file} as the config file.")

    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            print(f"Successfully loaded PATHs from {config_file}.")
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Error loading config: {e}")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format in {config_file}: {e}")
    return None


def is_file_empty(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read(1) == ''  # Read one character



def setup_logger(name : str, log_file: Path, level: int = logging.INFO, filemode: str = 'w', encoding: str = 'utf-8') -> Logger:
    """Function to set up a logger for a specific file with filemode and encoding."""
    logger = logging.getLogger(name)
    handler = logging.FileHandler(log_file, mode=filemode, encoding=encoding)  
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
