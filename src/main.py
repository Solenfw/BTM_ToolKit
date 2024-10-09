from BTM_Quote_Tool.config import *
from BTM_Quote_Tool.file_operations import *
from BTM_Quote_Tool.matcher import find_best_match
import time
import logging

logging.basicConfig(
    filename='main_workflow.log',
    level=logging.INFO,
    filemode='w',
    encoding='utf-8'
)
import time
import logging

logging.basicConfig(
    filename='main_workflow.log',
    level=logging.INFO,
    filemode='w',
    encoding='utf-8'
)


def main():
    _exe = time.time()
    _exe = time.time()
    config = load_config()
    product_data = init_environment(config)
    logging.info("DONE : init config paths and env.")

    logging.info("DONE : init config paths and env.")

    keywords = load_input(config, "input_file")
    logging.info("DONE : retrieved inputs. ")

    product_codes, matched_products = find_best_match(keywords, product_data)
    save_output(config, "output_code_file", product_codes)
    save_output(config, "output_product_file", matched_products)
    logging.info(f"DONE : write code & product to relevant output files.")

    logging.info(f"DONE : write code & product to relevant output files.")

    # open for review
    # os.system(f"notepad {Path(config['output_code_file']).resolve()}")
    _end = time.time()
    time_spent = _end - _exe
    logging.info (f"Execution time: {time_spent:.2f} seconds")
    print("DONE!")

if __name__ == "__main__":
    main()

