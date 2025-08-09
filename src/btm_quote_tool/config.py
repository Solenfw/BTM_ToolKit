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


def data_processor(file_path: Path) -> dict:
    sheet_dict = {}

    # Read the CSV file using the csv module
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        unique_counter = 0
        next(csv_reader)
        for row in csv_reader:
            # Assuming the CSV has at least 3 columns
            code = row[0].strip()
            eng_descript = string_cleaner(row[1])
            vn_descript = string_cleaner(row[2])

            # Ensure unique key for duplicate Vietnamese descriptions
            key = vn_descript if vn_descript not in sheet_dict else f"{unique_counter}-{vn_descript}"
            sheet_dict[key] = (eng_descript, code)
            unique_counter += 1 if vn_descript in sheet_dict else 0
            
    return sheet_dict



def is_file_empty(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read(1) == ''  # Read one character



def init_environment(log : Path, config : object) -> dict | None:
    # general_log = setup_logger(Path('log/workflow.log'))
    """Sets up the environment and retrieves the necessary product data."""
    # Enter products needed for matching
    user_input_path = Path(config['tests']['input_file']).resolve()
    if is_file_empty(user_input_path):
        os.system(f"notepad {user_input_path}")

    product_file_path = Path(config['csv_source']["kls_product_csv"]).resolve()
    try:
        product_data = data_processor(product_file_path)
        log.info("DONE : Dataset fully loaded & cleaned.")
        return product_data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None


def setup_logger(name : str, log_file: Path, level: int = logging.INFO, filemode: str = 'w', encoding: str = 'utf-8') -> Logger:
    """Function to set up a logger for a specific file with filemode and encoding."""
    logger = logging.getLogger(name)
    handler = logging.FileHandler(log_file, mode=filemode, encoding=encoding)  
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
