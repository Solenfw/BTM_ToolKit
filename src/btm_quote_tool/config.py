import json
import os
from pathlib import Path
import pandas as pd
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


def load_config(config_file="config.json") -> object:
    """Loads PATH configuration from a JSON file."""
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Error loading config: {e}")
        return None


def data_processor(file_path: Path) -> dict:
    sheet_dict = {}
    data_raw = pd.read_excel(file_path)

    # Process the columns
    data_raw['col_a_value'] = data_raw.iloc[:, 0].astype(str).str.strip().str.lower()  # Column A
    data_raw['col_b_value'] = data_raw.iloc[:, 1].astype(str).str.strip().str.lower()  # Column B
    data_raw['col_c_value'] = data_raw.iloc[:, 2].astype(str).str.strip().str.lower()  # Column C

    unique_counter = 0
    for index, row in data_raw.iterrows():
        code = row['col_a_value']
        eng_descript = row['col_b_value']
        vn_descript = row['col_c_value']

        key = vn_descript if vn_descript not in sheet_dict else f"{unique_counter}-{vn_descript}"
        sheet_dict[key] = (eng_descript, code)
        unique_counter += 1 if vn_descript in sheet_dict else 0
    return sheet_dict



def is_file_empty(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read(1) == ''  # Read one character



def init_environment(config):
    """Sets up the environment and retrieves the necessary product data."""
    # Enter products needed for matching
    user_input_path = Path(config['tests']['input_file']).resolve()
    if is_file_empty(user_input_path):
        os.system(f"notepad {user_input_path}")

    product_file_path = Path(config['data_source']["product_data"]).resolve()
    try:
        product_data = data_processor(product_file_path)
        return product_data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None