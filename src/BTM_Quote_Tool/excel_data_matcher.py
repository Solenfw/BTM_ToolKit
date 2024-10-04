import os
import re
from excel_data_processor import file_process
from fuzzywuzzy import fuzz
from pathlib import Path
import json

class Color:
    CYAN = '\033[1;96m'
    YELLOW = '\033[1;33m'
    MAGENTA = '\033[1;35m'
    END = '\033[0m'
    
    @staticmethod
    def wrap_text(text, color):
        return f"{color}{text}{Color.END}"


# Special substring replacements for better matching
substring_replacements = {
    'xám' : 'bạc',
    'nhíp': 'kẹp',
    'nhíp mô': 'kẹp phẫu tích mô',
    'kẹp mang kim': 'kìm kẹp kim',
    'kẹp động mạch': 'kẹp mạch máu',
    'cán dao mổ': 'cán dao phẫu thuật',
    'nẩy xương': 'bẩy xương',
    'khay đựng hình quả thận': 'đĩa thận',
    'vén não': 'thìa phẫu thuật',
    'vén rễ thần kinh': 'móc',
    'vòng giữ dụng cụ có cán vòng' : 'kim băng cài giữ dụng cụ',
    'đáy hộp đựng và bảo quản dụng cụ phẫu thuật' : 'đáy hộp đựng và bảo quản dụng cụ marsafe',
    'khay lưới bảo quản dụng cụ phẫu thuật' : 'khay lưới đựng dụng cụ',
    'nắp hộp đựng và bảo quản dụng cụ phẫu thuật' : 'nắp hộp đựng và bảo quản dụng cụ marsafe'
}


def load_config(config_file="config.json"):
    """Loads configuration from a JSON file."""
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Error loading config: {e}")
        return None


def init_environment(config):
    """Sets up the environment and retrieves the necessary product data."""
    os.system("")  # Enables ANSI escape characters
    
    product_file_path = Path(config["product_file"]).resolve()
    try:
        product_data = file_process(product_file_path)
        return product_data
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None


def load_input(file_path):
    """Loads input keywords from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []


def save_output(file_path: str, data: list):
    """Saves the output data (codes or descriptions) to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for result in data:
            file.write(f"{result}\n")


def clean_string(text: str) -> str:
    """Cleans and standardizes input text for comparison."""
    text = re.sub(r'[^\w\s]', '', text)                 # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip().lower()    # Normalize whitespace and case
    
    # Apply substring replacements
    for original_text, replacement_text in substring_replacements.items():
        text = text.replace(original_text, replacement_text)
    return text


def all_keywords_exist(keywords: list, check_string: str) -> bool:
    """Checks if all words from a keyword are present in the target string."""
    return all(keyword in check_string for keyword in keywords)


def calculate_similarity(keyword: str, product: str) -> int:
    """Validates and scores the similarity between a keyword and a product description."""
    keyword = clean_string(keyword)
    product = clean_string(product)

    # Check for a perfect match based on word containment
    keywords = keyword.split()
    if all_keywords_exist(keywords, product):
        return 100

    # Use fuzzy matching for partial matches
    return fuzz.token_set_ratio(keyword, product)


def find_best_match(keywords, product_data):
    """Finds the best matching product for each keyword."""
    product_codes = []
    matched_products = []
    color = Color()

    for keyword in keywords:
        print(f"{color.CYAN} ---------- {keyword} -------------- {color.END}")
        best_match = None
        best_score = 0

        for description in product_data.keys():
            similarity_score = calculate_similarity(keyword, description)
            if similarity_score >= 70 and similarity_score > best_score:
                best_score = similarity_score
                best_match = description

        if best_match:
            print(color.YELLOW + "Match found." + color.END)
            matched_products.append(best_match)
            product_codes.append(product_data[best_match][1])  
        else:
            print("No match.")
            product_codes.append("NONE")
            matched_products.append('NONE')
    
    return product_codes, matched_products


def main():
    config = load_config()

    if config is None:
        return

    product_data = init_environment(config)

    # initiate file paths
    input_file_path = Path(config["input_file"]).resolve()
    output_code_file = Path(config["output_code_file"]).resolve()
    output_product_file = Path(config["output_product_file"]).resolve()

    # Get input
    os.system(f"notepad {input_file_path}")

    if product_data is None:
        return

    keywords = load_input(input_file_path)
    if not keywords:
        print("No keywords found to process.")
        return

    product_codes, matched_products = find_best_match(keywords, product_data)
    save_output(output_code_file, product_codes)
    save_output(output_product_file, matched_products)

    # Open output file in notepad for review
    os.system(f"notepad {output_code_file}")
    os.system(f"notepad {output_product_file}")


if __name__ == '__main__':
    main()
