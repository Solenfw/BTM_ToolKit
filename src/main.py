import os
from pathlib import Path
from BTM_Quote_Tool.config import load_config, init_environment
from BTM_Quote_Tool.file_operations import load_input, save_output
from BTM_Quote_Tool.matcher import find_best_match




def main():
    config = load_config()
    product_data = init_environment(config)
    keywords = load_input(config, "input_file")
    product_codes, matched_products = find_best_match(keywords, product_data)
    save_output(config, "output_code_file", product_codes)
    save_output(config, "output_product_file", matched_products)
    # open for review
    os.system(f"notepad {Path(config['output_code_file']).resolve()}")


if __name__ == "__main__":
    main()

