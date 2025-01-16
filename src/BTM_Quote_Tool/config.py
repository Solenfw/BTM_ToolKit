import json
import logging
from logging import Logger
import os
from pathlib import Path
import csv
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from .string_utilities import string_cleaner

def load_config(config_file="config.json") -> object:
    """Loads PATH configuration from a JSON file."""
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            print("successfully loaded PATHs from Json.")
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Error loading config: {e}")
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
