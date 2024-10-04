import os
import re
import sys
import pandas as pd

os.system("")
class Color:
    CYAN = '\033[1;96m'
    YELLOW = '\033[1;33m'
    MAGENTA = '\033[1;35m'
    RED = '\033[1;31m'
    END = '\033[0m'
    
    @staticmethod
    def wrap_text(text, color):
        return f"{color}{text}{Color.END}"


def file_process(file_path: str) -> dict:
    """Processes the Excel file and returns a dictionary of product descriptions and their details."""
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


def display(color: Color, product: str, stats: list):
    """Displays the product description, English description, and code with formatting."""
    descript = re.sub(r'(\d+)', color.wrap_text(r'\1', Color.MAGENTA), product)
    eng_descript = re.sub(r'(\d+)', color.wrap_text(r'\1', Color.MAGENTA), stats[0])
    code = stats[1]
    print(f"_ {descript.ljust(70)}    {color.CYAN}{eng_descript.ljust(65)}{color.END}    {color.YELLOW}{code.ljust(25)}{color.END}")


def all_keys_exist(keys: list, check_string: str) -> bool:
    """Returns True if all keys exist in the check string."""
    return all(key in check_string for key in keys)


def none_keys_exist(words: list, target: str) -> bool:
    """Returns True if none of the words exist in the target string."""
    return not any(word in target for word in words)


def get_input(prompt: str) -> str:
    """Safely gets input from the user."""
    try:
        return input(prompt)
    except EOFError:
        return ''


def search_by_code(sig_key: str, sheet_dict: dict, color: Color):
    """Searches for products by matching the code exactly."""
    for prd_descript, stats in sheet_dict.items():
        if stats[1] == sig_key:
            display(color, prd_descript, stats)
            return True
    return False


def product_search(sig_key: str, exclude_words: list, sheet_dict: dict) -> dict:
    """Performs the product search based on significant keywords and exclusion."""
    matching_products = {}
    sig_key_list = sig_key.strip().lower().split()

    for prd_descript, stats in sheet_dict.items():
        if all_keys_exist(sig_key_list, prd_descript) and none_keys_exist(exclude_words, prd_descript):
            matching_products[prd_descript] = stats
    return matching_products


def process_command(sheet_dict: dict):
    color = Color()
    while True:
        command = get_input("Command (1 to start, 0 to terminate): ").strip()

        if command == '0':
            print("Terminating. . . ")
            sys.exit(0)

        if command == '1':
            print(f"Report:\nNumber of items Information acquired: {len(sheet_dict)}\nProceeding. . .")

            while True:
                sig_key = get_input(color.wrap_text("Enter sigKey(s): ", Color.RED)).strip()
                if sig_key.lower() == 'end':
                    print("Terminating. . . ")
                    sys.exit(0)

                exclude_words = get_input("Exclude: ").strip().lower().split()

                # Clear screen or check by code if entered
                if sig_key.lower() in ['cls', 'clear']:
                    os.system('cls')
                    continue

                if re.fullmatch(r'\d{2}-\d{3}-\d{2}-\d{2}', sig_key):
                    if search_by_code(sig_key, sheet_dict, color):
                        continue

                matching_products = product_search(sig_key, exclude_words, sheet_dict)

                if not matching_products:
                    print("No match found for sigKey(s).")
                    if get_input("Re-enter sigKey(s) or 0 to terminate: ") == '0':
                        sys.exit(0)
                else:
                    detail = get_input("Detail (optional): ").strip().lower()
                    if detail:
                        details_list = detail.split()
                        matching_products = {prd: stats for prd, stats in matching_products.items()
                                             if all_keys_exist(details_list, stats[0])}

                    if not matching_products:
                        print("No match found with provided details.")
                    else:
                        for prd_descript, stats in matching_products.items():
                            display(color, prd_descript, stats)


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    product_file_path = os.path.join(script_dir, '..', '..', 'data', 'DANH MUC SP KLS MARTIN_updated.xlsx')
    product_file_path = os.path.abspath(product_file_path)
    sheet_dict = file_process(product_file_path)
    process_command(sheet_dict)
