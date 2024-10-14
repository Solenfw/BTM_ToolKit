import logging
from pathlib import Path
import time
from BTM_Quote_Tool.config import load_config, init_environment
from BTM_Quote_Tool.file_operations import save_output, load_input
from BTM_Quote_Tool.matcher import find_best_match


logging.basicConfig(
    filename='main_workflow.log',
    filemode='w',
    encoding='utf-8'
)


def main():
    config = load_config()
    product_data = init_environment(config)
    input_file_path = Path(config['tests']['input_file']).resolve()
    keywords = load_input(config, 'tests', 'input_file')
    logging.info("DONE : prep inputs & env.")
    _start = time.time()
    product_codes, product_matches = find_best_match(keywords, product_data)
    save_output(config, 'tests', 'output_code_file', product_codes)
    save_output(config, 'tests', 'output_product_file', product_matches)
    _end = time.time()
    logging.info("DONE : Matching terminated. ")
    execution_time = _end - _start
    logging.info(f"Execution time : {execution_time}")
    
    with open(input_file_path, 'w'):
        pass
    print("DONE!.")


if __name__ == '__main__':
    main()
