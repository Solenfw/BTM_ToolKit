import json
import os
from pathlib import Path
import pandas as pd


def load_config(config_file="config.json") -> object:
    """Loads PATH configuration from a JSON file."""
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Error loading config: {e}")
        return None



def data_processor(file_path: str) -> dict:
    """Processes Excel file (spec format) and returns a dictionary of product descriptions and their details."""
    sheet_dict = {}
    data_raw = pd.read_excel(file_path)
    data_raw['col_a_value'] = data_raw.iloc[:, 0].astype(str).str.strip().str.lower()  # Column A
    data_raw['col_b_value'] = data_raw.iloc[:, 1].astype(str).str.strip().str.lower()  # Column B
    data_raw['col_c_value'] = data_raw.iloc[:, 2].astype(str).str.strip().str.lower()  # Column C

    unique_counter = 0
    for row in data_raw.itertuples(index=False):
        code = row.col_a_value
        eng_descript = row.col_b_value
        vn_descript = row.col_c_value

        key = vn_descript if vn_descript not in sheet_dict else f"{unique_counter}-{vn_descript}"
        sheet_dict[key] = [eng_descript, code]
        unique_counter += 1 if vn_descript in sheet_dict else 0

    return sheet_dict


def init_environment(config):
    """Sets up the environment and retrieves the necessary product data."""
    # Enter products needed for matching
    os.system(f"notepad {Path(config["input_file"]).resolve()}")
    
    product_file_path = Path(config["product_data"]).resolve()
    try:
        product_data = data_processor(product_file_path)
        return product_data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None