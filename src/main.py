from pathlib import Path
import time
from BTM_Quote_Tool.config import load_config, init_environment, setup_logger
from BTM_Quote_Tool.file_operations import save_output, load_input
from BTM_Quote_Tool.matcher import find_best_match





def main():
    general_log = setup_logger('general', Path('log/workflow.log'))
    score_log = setup_logger('score', Path('log/scores.log'))
    _start = time.time()
    config = load_config()
    product_data = init_environment(general_log, config)
    keywords = load_input(config, 'tests', 'input_file')
    general_log.info("DONE : prep inputs & env.")
    product_codes, product_matches = find_best_match(general_log, score_log, keywords, product_data)
    save_output(config, 'tests', 'output_code_file', product_codes)
    save_output(config, 'tests', 'output_product_file', product_matches)
    _end = time.time()
    general_log.info("DONE : Matching terminated. ")
    execution_time = _end - _start
    general_log.info(f"Execution time : {execution_time:.2f} s")
    # input_file_path = Path(config['tests']['input_file']).resolve()
    # with open(input_file_path, 'w'):
    #     pass
    print("DONE!.")


if __name__ == '__main__':
    main()
